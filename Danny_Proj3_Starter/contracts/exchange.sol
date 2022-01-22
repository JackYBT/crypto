// =================== CS251 DEX Project =================== // 
//        @authors: Simon Tao '22, Mathew Hogan '22          //
// ========================================================= //    
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import '../interfaces/erc20_interface.sol';
import '../libraries/safe_math.sol';
import './token.sol';


contract TokenExchange {
    using SafeMath for uint;
    address public admin;

    address tokenAddr = 0xf263AaF8C8ab2F293D2394a3157b45a0D451f969;                              // TODO: Paste token contract address here.
    RamonToken private token = RamonToken(tokenAddr);         // TODO: Replace "Token" with your token class.             

    // Liquidity pool for the exchange
    uint public token_reserves = 0;
    uint public eth_reserves = 0;

    // Constant: x * y = k
    uint public k;
    
    // liquidity rewards
    uint private swap_fee_numerator = 2;       // TODO Part 5: Set liquidity providers' returns.
    uint private swap_fee_denominator = 100;
    
    // liquidity share
    uint private total_liquidity = 0;
    mapping(address => uint) liquidity;
    
    // decimal constant 10^8
    uint private decimal_constant = 100000000;
    
    // uninvested fees
    uint uninvested_eth = 0;
    uint uninvested_token = 0;
    
    event AddLiquidity(address from, uint amount);
    event RemoveLiquidity(address to, uint amount);
    event Received(address from, uint amountETH);

    constructor() 
    {
        admin = msg.sender;
    }
    
    modifier AdminOnly {
        require(msg.sender == admin, "Only admin can use this function!");
        _;
    }

    // Used for receiving ETH
    receive() external payable {
        emit Received(msg.sender, msg.value);
    }
    fallback() external payable{}

    // Function createPool: Initializes a liquidity pool between your Token and ETH.
    // ETH will be sent to pool in this transaction as msg.value
    // amountTokens specifies the amount of tokens to transfer from the liquidity provider.
    // Sets up the initial exchange rate for the pool by setting amount of token and amount of ETH.
    function createPool(uint amountTokens)
        external
        payable
        AdminOnly
    {
        // require pool does not yet exist
        require (token_reserves == 0, "Token reserves was not 0");
        require (eth_reserves == 0, "ETH reserves was not 0.");

        // require nonzero values were sent
        require (msg.value > 0, "Need ETH to create pool.");
        require (amountTokens > 0, "Need tokens to create pool.");

        token.transferFrom(msg.sender, address(this), amountTokens);
        eth_reserves = msg.value;
        token_reserves = amountTokens;
        k = eth_reserves.mul(token_reserves);

        // TODO: Keep track of the initial liquidity added so the initial provider
        //          can remove this liquidity
        total_liquidity = total_liquidity.add(amountTokens);
        liquidity[msg.sender] = amountTokens;
    }

    // ============================================================
    //                    FUNCTIONS TO IMPLEMENT
    // ============================================================
    /* Be sure to use the SafeMath library for all operations! */
    
    // Function priceToken: Calculate the price of your token in ETH.
    // You can change the inputs, or the scope of your function, as needed.
    function priceToken() 
        public 
        view
        returns (uint)
    {
        /******* TODO: Implement this function *******/
        /* HINTS:
            Calculate how much ETH is of equivalent worth based on the current exchange rate.
        */
        return decimal_constant.mul(eth_reserves).div(token_reserves);
    }

    // Function priceETH: Calculate the price of ETH for your token.
    // You can change the inputs, or the scope of your function, as needed.
    function priceETH()
        public
        view
        returns (uint)
    {
        /******* TODO: Implement this function *******/
        /* HINTS:
            Calculate how much of your token is of equivalent worth based on the current exchange rate.
        */
        return decimal_constant.mul(token_reserves).div(eth_reserves);
    }


    /* ========================= Liquidity Provider Functions =========================  */ 

    // Function addLiquidity: Adds liquidity given a supply of ETH (sent to the contract as msg.value)
    // You can change the inputs, or the scope of your function, as needed.
    function addLiquidity(uint max_exchange_rate, uint min_exchange_rate) 
        external 
        payable
    {
        /******* TODO: Implement this function *******/
        /* HINTS:
            Calculate the liquidity to be added based on what was sent in and the prices.
            If the caller possesses insufficient tokens to equal the ETH sent, then transaction must fail.
            Update token_reserves, eth_reserves, and k.
            Emit AddLiquidity event.
        */
        require(msg.value > 0, "addLiquidity ETH amount must be postive");
        
        //check min, max exchange rate 
        require(priceETH() < max_exchange_rate, "max exchange rate exceeded");
        require(priceETH() > min_exchange_rate, "min exchange rate exceeded");
        
        //amount of token required
        uint tokenAmount = priceETH().mul(msg.value).div(decimal_constant);
        
        //ensure user has sufficient tokens
        require(token.balanceOf(msg.sender) >= tokenAmount, "Insufficient RamonToken balance");
        
        //ensure we have permission to receive tokens
        require(token.allowance(msg.sender, address(this)) >= tokenAmount, "Insufficient allowance");
        
        //get tokens from sender
        bool received = token.transferFrom(msg.sender, address(this), tokenAmount);
        require(received, "Token transfer from LP failed");
        
        //adjust reserves
        token_reserves = token_reserves.add(tokenAmount);
        eth_reserves = eth_reserves.add(msg.value);
        k = token_reserves.mul(eth_reserves);
        
        //adjust liquidity tracker
        uint share = tokenAmount.mul(total_liquidity).div(token_reserves.sub(tokenAmount));
        total_liquidity = total_liquidity.add(share);
        liquidity[msg.sender] = liquidity[msg.sender].add(share);
        
        emit AddLiquidity(msg.sender, tokenAmount);
    }


    // Function removeLiquidity: Removes liquidity given the desired amount of ETH to remove.
    // You can change the inputs, or the scope of your function, as needed.
    function removeLiquidity(uint amountETH, uint max_exchange_rate, uint min_exchange_rate)
        public 
        payable
    {
        /******* TODO: Implement this function *******/
        /* HINTS:
            Calculate the amount of your tokens that should be also removed.
            Transfer the ETH and Token to the provider.
            Update token_reserves, eth_reserves, and k.
            Emit RemoveLiquidity event.
        */
        require(amountETH > 0, "removeLiquidity ETH amount must be postive");
        require(eth_reserves > amountETH, "Insufficient eth reserves");
        
        //calculate how much eth they own
        uint ethAmountOwned = eth_reserves.mul(liquidity[msg.sender]).div(total_liquidity);
        
        //make sure they own enough to withdraw
        require(ethAmountOwned >= amountETH, "sender does not own sufficient liquidity");
        
        //check min, max exchange rate 
        require(priceETH() < max_exchange_rate, "max exchange rate exceeded");
        require(priceETH() > min_exchange_rate, "min exchange rate exceeded");
        
        //amount of token they hope to withdraw
        uint amountToken = amountETH.mul(priceETH()).div(decimal_constant);
    
        //adjust reserve tracker
        token_reserves = token_reserves.sub(amountToken);
        eth_reserves = eth_reserves.sub(amountETH);
        k = token_reserves.mul(eth_reserves);
        
        //adjust liquidity tracker
        uint share = total_liquidity.mul(amountToken).div(token_reserves);
        total_liquidity = total_liquidity.sub(share);
        liquidity[msg.sender] = liquidity[msg.sender].sub(share);
        
        //send token back to user
        bool tokenSent = token.transfer(msg.sender, amountToken);
        require(tokenSent, "Failed to send RamonToken to LP");
        
        //send eth back to user
        (bool sent, bytes memory data) = payable(msg.sender).call{value: amountETH}("returning liquidity");
        require(sent, "Failed to send Ether to LP");
        
        emit RemoveLiquidity(msg.sender, amountToken);
    }

    // Function removeAllLiquidity: Removes all liquidity that msg.sender is entitled to withdraw
    // You can change the inputs, or the scope of your function, as needed.
    function removeAllLiquidity(uint max_exchange_rate, uint min_exchange_rate)
        external
        payable
    {
        /******* TODO: Implement this function *******/
        /* HINTS:
            Decide on the maximum allowable ETH that msg.sender can remove.
            Call removeLiquidity().
        */
        uint ethAmountOwned = eth_reserves.mul(liquidity[msg.sender]).div(total_liquidity);
        
        // what happens if they own all of the liquidity?
        removeLiquidity(ethAmountOwned, max_exchange_rate, min_exchange_rate);
    }

    /***  Define helper functions for liquidity management here as needed: ***/



    /* ========================= Swap Functions =========================  */ 

    // Function swapTokensForETH: Swaps your token with ETH
    // You can change the inputs, or the scope of your function, as needed.
    function swapTokensForETH(uint amountTokens, uint max_eth_token_rate)
        external 
        payable
    {
        /******* TODO: Implement this function *******/
        /* HINTS:
            Calculate amount of ETH should be swapped based on exchange rate.
            Transfer the ETH to the provider.
            If the caller possesses insufficient tokens, transaction must fail.
            If performing the swap would exhaus total ETH supply, transaction must fail.
            Update token_reserves and eth_reserves.

            Part 4: 
                Expand the function to take in addition parameters as needed.
                If current exchange_rate > slippage limit, abort the swap.
            
            Part 5:
                Only exchange amountTokens * (1 - liquidity_percent), 
                    where % is sent to liquidity providers.
                Keep track of the liquidity fees to be added.
        */
        require(amountTokens > 0, "Must be positive input");
        uint fee_token = amountTokens.mul(swap_fee_numerator).div(swap_fee_denominator);
        
        //check if fee can be invested
        if (uninvested_eth > 0) {
            
            // more tokens than eth reserves, invest all eth
            if (fee_token.mul(priceToken()).div(decimal_constant) > uninvested_eth) {
                //adjust reserves
                uint investedTokens = priceETH().mul(uninvested_eth).div(decimal_constant);
                token_reserves = token_reserves.add(investedTokens);
                eth_reserves = eth_reserves.add(uninvested_eth);
                k = token_reserves.mul(eth_reserves);
                
                //update uninvested reserves
                uninvested_eth = 0;
                uninvested_token = uninvested_token.add(fee_token.sub(investedTokens));
                
            // fewer token than eth reserves, all tokens invested
            } else {
                uint investedEth = priceToken().mul(fee_token).div(decimal_constant);
                token_reserves = token_reserves.add(fee_token);
                eth_reserves = eth_reserves.add(investedEth);
                k = token_reserves.mul(eth_reserves);
                
                //update uninvested reserves
                uninvested_eth = uninvested_eth.sub(investedEth);
            }
        } else {
            uninvested_token = uninvested_token.add(fee_token);
        }
        
        //calculate amount ETH we owe the user
        uint amountETH = eth_reserves.mul(amountTokens.sub(fee_token)).div(token_reserves.add(amountTokens.sub(fee_token)));
        
        require(amountETH < eth_reserves, "Insufficient eth pool reserves");
        require(decimal_constant.mul(amountTokens.sub(fee_token)).div(amountETH) < max_eth_token_rate, "Exchange rate above max. acceptable");
        
        //ensure user has sufficient tokens
        require(token.balanceOf(msg.sender) >= amountTokens, "Insufficient RamonToken balance");
        
        //ensure we have permission to receive tokens
        require(token.allowance(msg.sender, address(this)) >= amountTokens, "Insufficient allowance");
        
        bool received = token.transferFrom(msg.sender, address(this), amountTokens);
        require(received, "Failed to get ramon token from user");
        
        //send eth to user
        (bool sent, bytes memory data) = payable(msg.sender).call{value: amountETH}("swap for eth");
        require(sent, "Failed to send Ether to user");
        
        //make changes to reserves
        token_reserves = token_reserves.add(amountTokens.sub(fee_token));
        eth_reserves = eth_reserves.sub(amountETH);

        /***************************/
        // DO NOT MODIFY BELOW THIS LINE
        /* Check for x * y == k, assuming x and y are rounded to the nearest integer. */
        // Check for Math.abs(token_reserves * eth_reserves - k) < (token_reserves + eth_reserves + 1));
        //   to account for the small decimal errors during uint division rounding.
        uint check = token_reserves.mul(eth_reserves);
        if (check >= k) {
            check = check.sub(k);
        }
        else {
            check = k.sub(check);
        }
        assert(check < (token_reserves.add(eth_reserves).add(1)));
    }



    // Function swapETHForTokens: Swaps ETH for your tokens.
    // ETH is sent to contract as msg.value.
    // You can change the inputs, or the scope of your function, as needed.
    function swapETHForTokens(uint min_eth_token_rate)
        external
        payable 
    {
        /******* TODO: Implement this function *******/
        /* HINTS:
            Calculate amount of your tokens should be swapped based on exchange rate.
            Transfer the amount of your tokens to the provider.
            If performing the swap would exhaus total token supply, transaction must fail.
            Update token_reserves and eth_reserves.

            Part 4: 
                Expand the function to take in addition parameters as needed.
                If current exchange_rate > slippage limit, abort the swap. 
            
            Part 5: 
                Only exchange amountTokens * (1 - %liquidity), 
                    where % is sent to liquidity providers.
                Keep track of the liquidity fees to be added.
        */
        require(msg.value > 0, "Must be positive input");
        uint fee_eth = msg.value.mul(swap_fee_numerator).div(swap_fee_denominator);
        uint amountEth = msg.value - fee_eth;
        
        //check if fee can be invested
        if (uninvested_token > 0) {
            if (fee_eth.mul(priceETH()).div(decimal_constant) > uninvested_token) {
                //adjust reserves
                uint investedEth = priceToken().mul(uninvested_token).div(decimal_constant);
                token_reserves = token_reserves.add(uninvested_token);
                eth_reserves = eth_reserves.add(investedEth);
                k = token_reserves.mul(eth_reserves);
                
                //update uninvested reserves
                uninvested_token = 0;
                uninvested_eth = uninvested_eth.add(fee_eth.sub(investedEth));
                
            // fewer eth than token reserves, all eth invested
            } else {
                uint investedToken = priceETH().mul(fee_eth).div(decimal_constant);
                token_reserves = token_reserves.add(investedToken);
                eth_reserves = eth_reserves.add(fee_eth);
                k = token_reserves.mul(eth_reserves);
                
                //update uninvested reserves
                uninvested_token = uninvested_token.sub(investedToken);
            }
        } else {
            uninvested_eth = uninvested_eth.add(fee_eth);
        }
        
        
        //calculate amount of tokens to give out
        uint amountTokens = token_reserves.mul(amountEth).div(eth_reserves.add(amountEth));
        require(amountTokens < token_reserves, "Insufficient token pool reserves");
        require(decimal_constant.mul(amountTokens).div(amountEth) > min_eth_token_rate, "Exchange rate below min. acceptable");
        
        //send tokens to user
        bool tokenSent = token.transfer(msg.sender, amountTokens);
        require(tokenSent, "Failed to send RamonToken to user");
        
        //update reserves
        token_reserves = token_reserves.sub(amountTokens);
        eth_reserves = eth_reserves.add(amountEth);

        /**************************/
        // DO NOT MODIFY BELOW THIS LINE
        /* Check for x * y == k, assuming x and y are rounded to the nearest integer. */
        // Check for Math.abs(token_reserves * eth_reserves - k) < (token_reserves + eth_reserves + 1));
        //   to account for the small decimal errors during uint division rounding.
        uint check = token_reserves.mul(eth_reserves);
        if (check >= k) {
            check = check.sub(k);
        }
        else {
            check = k.sub(check);
        }
        assert(check < (token_reserves.add(eth_reserves).add(1)));
    }

    /***  Define helper functions for swaps here as needed: ***/

}
