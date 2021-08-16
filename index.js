const protobuf = require("protobufjs");

const fromHexString = hexString =>
    new Uint8Array(hexString.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));

// Run coffee.py to regenerate
const OLD_FASHIONED_COFFEE_HEX = "0a1b0000001749276d2062657474657220776974686f7574206d696c6b120d6c6f63616c5f6f61746d696c6b1a020001";

const run = async () => {
    const root = await protobuf.load("beverage.proto");
    const OldFashionedCoffee = root.lookupType("test.OldFashionedCoffee");

    const encodedPayload = fromHexString(OLD_FASHIONED_COFFEE_HEX);
    const decodedPayload = OldFashionedCoffee.decode(encodedPayload);

    const errMsg = OldFashionedCoffee.verify(decodedPayload);
    if (errMsg)
        throw Error(errMsg);
    console.log({decodedPayload})

    const message1 = OldFashionedCoffee.create(decodedPayload); // or use .fromObject if conversion is necessary

    const buffer = OldFashionedCoffee.encode(message1).finish();
    const message2 = OldFashionedCoffee.decode(buffer);
    const object = OldFashionedCoffee.toObject(message2);
    console.log({object});
}


run();
