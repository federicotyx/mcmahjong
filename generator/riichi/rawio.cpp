#include "rawio.hpp"

namespace wat
{
	void read_raw(std::istream& is, std::string& s)
	{
		char c;
		for (c = read_raw<char>(is); c != '\0'; c = read_raw<char>(is))
		{
			s.push_back(c);
		}
	}

	void write_raw(std::ostream& os, const std::string& s)
	{
		for (int i = 0; i < s.size(); ++i)
		{
			write_raw(os, s[i]);
		}
		write_raw(os, '\0');
	}
}
