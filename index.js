const protobuf = require("protobufjs");

const toHexString = buffer =>
    [...new Uint8Array(buffer)]
        .map(b => b.toString(16).padStart(2, "0"))
        .join("")

const fromHexString = hexString =>
    new Uint8Array(hexString.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));

// Run coffee.py to regenerate
const OLD_FASHIONED_COFFEE_HEX = "0a1b0000001749276d2062657474657220776974686f7574206d696c6b120d6c6f63616c5f6f61746d696c6b1a020001";
const BLEND_HEX = '0000001749276d2062657474657220776974686f7574206d696c6b';
const MILK_TYPE_HEX = '6c6f63616c5f6f61746d696c6b';
const SIZE_HEX = '0001'

const run = async () => {
    const root = await protobuf.load("beverage.proto");
    const OldFashionedCoffee = root.lookupType("coffee.OldFashionedCoffee");

    const encodedPayload = fromHexString(OLD_FASHIONED_COFFEE_HEX);
    const decodedPayload = OldFashionedCoffee.decode(encodedPayload);

    const errMsg = OldFashionedCoffee.verify(decodedPayload);
    if (errMsg)
        throw Error(errMsg);
    console.log({decodedPayload})

    console.assert(toHexString(decodedPayload.blend) === BLEND_HEX)
    console.assert(toHexString(decodedPayload.milkType) === MILK_TYPE_HEX)
    console.assert(toHexString(decodedPayload.size) === SIZE_HEX)


    const message1 = OldFashionedCoffee.create(decodedPayload);
    const buffer = OldFashionedCoffee.encode(message1).finish();
    const message2 = OldFashionedCoffee.decode(buffer);
    const object = OldFashionedCoffee.toObject(message2);
    console.log({object})
}


run();
