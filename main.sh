#!/bin/bash

mkdir clase12

touch clase12/file{1..500}.txt

mkdir clase13

mv clase12/file*.txt clase13/

ls clase13/ | wc -l


