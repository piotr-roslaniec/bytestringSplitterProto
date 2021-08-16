# bytestringSplitterProto

Generate protobuf schema from `bytestring-splitter` classes.

* Annotate factory classes with `@serializable`
* Generate `.proto` file
* Serialize `bytestring-splitter` classes to protobuf `Message` objects
* Deserialize those objects using JavaScript

# Installation

Install protobuf

```bash
cd /tmp
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.12.4/protobuf-all-3.12.4.tar.gz
tar -xzf protobuf-all-3.12.4.tar.gz
cd protobuf-3.12.4/ && ./configure && make && sudo make install

# You may need to reload shared libs
# sudo ldconfig

protoc --version
```

Install `bytestringSplitter`

```bash
pip install bytestring-splitter 
```

# Usage

Generate protobuf schema

```bash
python generator.py
```

Generate Python protobuf code

```bash
protoc --proto_path=. --python_out=. beverage.proto
```

Run Python example

```bash
python coffee.py
```

Run JS example

```bash
npm run test
```

