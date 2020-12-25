#!/bin/bash

git checkout --detach
git reset --soft $1
git checkout $1
