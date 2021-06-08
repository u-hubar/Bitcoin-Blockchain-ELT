CREATE TABLE Blockchain.Blocks
(
  blockHash VARCHAR(256) NOT NULL,
  size BIGINT NOT NULL,
  mainChain BOOLEAN NOT NULL,
  height BIGINT NOT NULL,
  txNum INT NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  prevBlock VARCHAR(256)
);

ALTER TABLE Blockchain.Blocks ADD CONSTRAINT PK_Blocks
  PRIMARY KEY (blockHash);

CREATE TABLE Blockchain.Addresses
(
  address VARCHAR(256) NOT NULL,
  balance BIGINT NOT NULL,
  isMiner BOOLEAN,
  entity BIGINT
);

ALTER TABLE Blockchain.Addresses ADD CONSTRAINT PK_Addresses
  PRIMARY KEY (address);

CREATE TABLE Blockchain.Transactions
(
  txhash VARCHAR(256) NOT NULL,
  timestamp TIMESTAMP,
  blockHash VARCHAR(256),
  ip VARCHAR(256)
);

ALTER TABLE Blockchain.Transactions ADD CONSTRAINT PK_Transactions
  PRIMARY KEY (txhash);

CREATE TABLE Blockchain.inputSection
(
  txhash VARCHAR(256) NOT NULL,
  address VARCHAR(256) NOT NULL,
  amount BIGINT NOT NULL,
  hasScript BOOLEAN NOT NULL
);

CREATE TABLE Blockchain.outputSection
(
  txhash VARCHAR(256) NOT NULL,
  address VARCHAR(256) NOT NULL,
  amount BIGINT NOT NULL,
  hasScript BOOLEAN NOT NULL,
  unspent BOOLEAN NOT NULL,
  isMining BOOLEAN NOT NULL
);

CREATE TABLE Blockchain.Entities
(
  txhash VARCHAR(256) NOT NULL,
  address VARCHAR(256) NOT NULL
 
);

ALTER TABLE Blockchain.Transactions ADD CONSTRAINT fk_transaction_block
  FOREIGN KEY (blockHash) REFERENCES Blockchain.Blocks (blockHash);

ALTER TABLE Blockchain.inputSection ADD CONSTRAINT fk_input_transaction
  FOREIGN KEY (txhash) REFERENCES Blockchain.Transactions (txhash);

ALTER TABLE Blockchain.outputSection ADD CONSTRAINT fk_output_transaction
  FOREIGN KEY (txhash) REFERENCES Blockchain.Transactions (txhash);
  
ALTER TABLE Blockchain.inputSection ADD CONSTRAINT fk_input_address
  FOREIGN KEY (address) REFERENCES Blockchain.Addresses (address);

ALTER TABLE Blockchain.outputSection ADD CONSTRAINT fk_output_address
  FOREIGN KEY (address) REFERENCES Blockchain.Addresses (address);
  
ALTER TABLE Blockchain.Entities ADD CONSTRAINT fk_entity_transaction
  FOREIGN KEY (txhash) REFERENCES Blockchain.Transactions (txhash); 
 
ALTER TABLE Blockchain.Entities ADD CONSTRAINT fk_entity_address
  FOREIGN KEY (address) REFERENCES Blockchain.Addresses (address);