#ifndef MCMJ_LIB_TILECONV_HPP
#define MCMJ_LIB_TILECONV_HPP 11

#include <string>
#include <vector>

std::string bin2txt(uint8_t a);
uint8_t txt2bin(const std::string& str);
uint8_t txt2bin(char a, char b);

void txt2bin(const std::string& str, std::vector<uint8_t>& v);

#endif
