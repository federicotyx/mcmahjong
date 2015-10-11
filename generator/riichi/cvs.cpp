#include "cvs.hpp"

std::string b2t(int8_t a)
{
	int8_t t = abs(a) % 64;
	bool r = abs(a) >= 64;
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
	return res;
}
