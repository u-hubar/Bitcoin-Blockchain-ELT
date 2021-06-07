CREATE TABLE Blockchain.Addresses
(
  address varchar(256) NOT NULL,
  balance bigint NOT NULL,
  isMiner boolean,
  entity bigint NOT NULL
);

ALTER TABLE Blockchain.Addresses ADD CONSTRAINT PK_Addresses
  PRIMARY KEY (address);

CREATE TABLE Blockchain.Transactions
(
  txhash varchar(256) NOT NULL,
  timestamp timestamp,
  blockhash varchar(256),
  ip varchar(256)
);

ALTER TABLE Blockchain.Transactions ADD CONSTRAINT PK_Transactions
  PRIMARY KEY (txhash);

CREATE TABLE Blockchain.inputSection
(
  txhash varchar(256) NOT NULL,
  address varchar(256) NOT NULL,
  amount bigint NOT NULL,
  hasScript boolean NOT NULL
);

CREATE TABLE Blockchain.outputSection
(
  txhash varchar(256) NOT NULL,
  address varchar(256) NOT NULL,
  amount bigint NOT NULL,
  hasScript boolean NOT NULL,
  unspent boolean NOT NULL,
  isMining boolean NOT NULL
);

CREATE TABLE Blockchain.Entities
(
  txhash varchar(256) NOT NULL,
  address varchar(256) NOT NULL
 
);

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