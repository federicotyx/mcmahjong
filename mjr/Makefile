CPPFLAGS=`pkg-config libxml++-2.6 --cflags`
CXXFLAGS=-std=c++11 -O2 -g
LDFLAGS=`pkg-config libxml++-2.6 --libs` -lstdc++
all:mjrt2b example
mjrt2b:mjrt2b.o bitbuff.o tileconv.o
example:example.o example.o tileconv.o
