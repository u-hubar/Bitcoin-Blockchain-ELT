#!/bin/bash
pg_dump -h 192.168.0.105 -p 5432 -U postgres -W -d blockchain > backups/blockchain.sql