#include "tileconv.hpp"

std::string bin2text(uint8_t a)
{
	int8_t t = a % 64;
	bool r = (a >= 64);
	std::string res;
	if (t < 9)
	{
		res += char(t) + '1';
		if (!r)
		{
			res += 'm';
		}
		else
		{
			res += 'M';
		}
	}
	else if (t < 18)
	{
		res += char(t) - 9 + '1';
		if (!r)
		{
			res += 'p';
		}
		else
		{
			res += 'P';
		}
	}
	else if (t < 27)
	{
		res += char(t) - 18 + '1';
		if (!r)
		{
			res += 's';
		}
		else
		{
			res += 'S';
		}
	}
	else if (t < 34)
	{
		res += char(t) - 27 + '1';
		if (!r)
		{
			res += 'z';
		}
		else
		{
			res += 'Z';
		}
	}
	else
	{
		res += char(t) - 34 + '1';
		res += 'h';
	}
	return res;
}
uint8_t txt2bin(const std::string& str)
{
	uint8_t idx = 0;
	switch (str[1])
	{
	case 'm':
		idx = 0;
		break;
	case 'M':
		idx = 0 + 64;
		break;
	case 'p':
		idx = 9;
		break;
	case 'P':
		idx = 9 + 64;
		break;
	case 's':
		idx = 18;
		break;
	case 'S':
		idx = 18 + 64;
		break;
	case 'z':
		idx = 27;
		break;
	case 'Z':
		idx = 27 + 64;
		break;
	case 'h':
		idx = 34;
		break;
	case 'H':
		idx = 34 + 64;
		break;
	}
	uint8_t res = str[0] - '0';
	return res + idx;
}
