include "./mimc.circom";

/*
 * IfThenElse sets `out` to `true_value` if `condition` is 1 and `out` to
 * `false_value` if `condition` is 0.
 *
 * It enforces that `condition` is 0 or 1.
 *
 */
template IfThenElse() {
    signal input condition;
    signal input true_value;
    signal input false_value;
    signal output out;
    signal helper_signal;

    //enforces condition is indeed 0 or 1 
    condition*(1-condition) === 0;

    helper_signal <== (1-condition)*false_value;
    //signal helper_signal_2 =true_value * condition; 
    out <== true_value*condition+helper_signal;//helper_signal_2 + helper_signal;

    // TODO
    // Hint: You will need a helper signal...
}

/*
 * SelectiveSwitch takes two data inputs (`in0`, `in1`) and produces two ouputs.
 * If the "select" (`s`) input is 1, then it inverts the order of the inputs
 * in the ouput. If `s` is 0, then it preserves the order.
 *
 * It enforces that `s` is 0 or 1.
 */
template SelectiveSwitch() {
    signal input in0;
    signal input in1;
    signal input s;
    signal output out0;
    signal output out1;

    component sub_circuit = IfThenElse();
    sub_circuit.condition <== s;
    sub_circuit.false_value <== in0;
    sub_circuit.true_value <== in1;
    
    out0 <== sub_circuit.out;

    component sub_circuit_2 = IfThenElse();
    sub_circuit_2.condition <== s;
    sub_circuit_2.false_value <== in1;
    sub_circuit_2.true_value <== in0;

    out1 <== sub_circuit_2.out
    
}

/*
 * Verifies the presence of H(`nullifier`, `nonce`) in the tree of depth
 * `depth`, summarized by `digest`.
 * This presence is witnessed by a Merle proof provided as
 * the additional inputs `sibling` and `direction`, 
 * which have the following meaning:
 *   sibling[i]: the sibling of the node on the path to this coin
 *               at the i'th level from the bottom.
 *   direction[i]: "0" or "1" indicating whether that sibling is on the left.
 *       The "sibling" hashes correspond directly to the siblings in the
 *       SparseMerkleTree path.
 *       The "direction" keys the boolean directions from the SparseMerkleTree
 *       path, casted to string-represented integers ("0" or "1").
 */
template Spend(depth) {
    signal input digest;
    signal input nullifier;
    signal private input nonce;
    signal private input sibling[depth];
    signal private input direction[depth];

    //1. SHA256 the nullifier and nonce
    component coins_that_needs_verification[depth+1];// = Mimc2();
    
    coins_that_needs_verification[0] = Mimc2();
    coins_that_needs_verification[0].in0 <== nullifier;
    coins_that_needs_verification[0].in1 <== nonce;


    component order_of_SHA256_input[depth];
    for (var i = 1; i < depth+1; ++i) {
        //If direction[i] is 1, I assume the sibling is on the left
        //Therefore, I must have the order of SHA256(sibling, prev_hash)
        //So going into it, I must assume SHA256(prev_hash, sibling), and if direction[i] is 1, I swap 
        order_of_SHA256_input[i-1] = SelectiveSwitch();
        order_of_SHA256_input[i-1].in0 <== coins_that_needs_verification[i-1].out;
        order_of_SHA256_input[i-1].in1 <== sibling[i-1];
        order_of_SHA256_input[i-1].s <== direction[i-1]

        coins_that_needs_verification[i] = Mimc2();
        coins_that_needs_verification[i].in0 <== order_of_SHA256_input[i-1].out0;
        coins_that_needs_verification[i].in1 <== order_of_SHA256_input[i-1].out1;
        //Call in the whether it's on the left or the right function

    }
    
    //verify if the public digest is equal to the computer the root
    digest === coins_that_needs_verification[depth].out// hashes[depth];

    //2. Verify that, if using the nonce + nullifier provided by the client, 
    //we would correctly reach the merkle root digest, that is public
    //We start with the SHA256 from the previous operation, and go all the way up

    //3. Verify if the resulting hash is equal to the public digest


    // TODO
}
component main = Spend(10);
