#include "random.hpp"
#include "mlfe.hpp"
#include <random>

namespace wat
{

	namespace _w_detail
	{
		mlfe<> engine;
	}

	uint64_t random_n(uint64_t n)
	{
		std::uniform_int_distribution<uint64_t> uid(0, n);
		return uid(_w_detail::engine);
	}

	std::string random_string(uint64_t size)
	{
		std::string res;
		for (uint64_t i = 0; i < size; ++i)
		{
			char t = random_n(25);
			t += 'a';
			res.push_back(t);
		}
		return res;
	}
}
