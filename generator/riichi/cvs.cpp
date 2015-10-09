#include "cvs.hpp"

std::string b2t(int8_t a)
{
	int8_t t = abs(a);
	std::string res;
	if (t < 9)
	{
		res += char(t) + '1';
		if (a >= 0)
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
		if (a > 0)
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
		if (a > 0)
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
		if (a > 0)
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