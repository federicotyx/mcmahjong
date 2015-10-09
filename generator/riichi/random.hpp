#ifndef _WAT_RANDOM_HPP
#define _WAT_RANDOM_HPP 11

#include <cstdint>
#include <string>
#include "mlfe.hpp"

///The wat namespace
namespace wat
{
	namespace _w_detail
	{
		extern mlfe<> engine;
	}

    ///a random in [0,1)
	template<typename Realtype = double>
    Realtype random_01()
	{
		static std::uniform_real_distribution<Realtype> urd(0, 1);
		return urd(_w_detail::engine);
	}

    ///a random in [0, n]
    uint64_t random_n(uint64_t n);

	//a random lower case string
	std::string random_string(uint64_t size);
}

#endif // _WAT_RANDOM_HPP
