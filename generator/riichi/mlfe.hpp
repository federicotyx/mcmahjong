#ifndef _WAT_MLFE_HPP
#define _WAT_MLFE_HPP 11
#include <iostream>
#include <cstdint>
#include <random>
#include <assert.h>

namespace wat
{
    ///Multiplicative Lagged Fibonacci Engine
    ///
    ///Return type is always uint64_t, and range is always \f$[0,2^{63}-1]\f$.
    ///Recommend set of (k,l) is (17,5),(55,24),(607,273),(1279,861).
    ///Increasing (k,l) will increase memory usage, random number quality, but do not influence the speed.
    ///The random number from random device will be used as seed, unless seed is provided
    template<int k = 1279, int l = 861>
    class mlfe
    {
    public:
        typedef uint64_t result_type;

        static constexpr size_t state_size = k;
        static constexpr size_t lag_size = l;

        ///using random device as seed
        mlfe();
        ///using the value as seed, it will using minstd_rand and uniform_int_distribution to do initialize
        explicit mlfe(uint64_t value);
        ///using the value in [first, last) as seed
        ///
        ///require last-first=k
        template<typename InputIterator>
        explicit mlfe(InputIterator first, InputIterator last);

        void seed(uint64_t value);
        template<typename InputIterator>
        void seed(InputIterator first, InputIterator last);

        static constexpr uint64_t min()
        {
            return 0ULL;
        };
        static constexpr uint64_t max()
        {
            return 0x7fffffffffffffffULL;
        };

        uint64_t operator()();

        ///get current state, for reproduce same sequence
        template<typename OutputIterator>
        void get_state(OutputIterator first, OutputIterator last);
    protected:
        uint64_t _state[k];
        int _si;
    };

    template<int k, int l>
    mlfe<k, l>::mlfe()
    {
        _si = 0;
        std::random_device rd;
        std::uniform_int_distribution<uint64_t> uid(0ULL, 0x7fffffffffffffffULL);
        bool flag = false;
        for (int i = 0; i < k; ++i)
        {
            _state[i] = (uid(rd) << 1) | 1ULL;
            if ((_state[i] & 0x2ULL) == 0x2ULL)
            {
                flag = true;
            }
        }
        if (!flag)
        {
            _state[0] |= 0x2ULL;
        }
    }

    template<int k, int l>
    mlfe<k, l>::mlfe(uint64_t value)
    {
        seed(value);
    }

    template<int k, int l> template<typename InputIterator>
    mlfe<k, l>::mlfe(InputIterator first, InputIterator last)
    {
        seed(first, last);
    }

    template<int k, int l>
    void mlfe<k, l>::seed(uint64_t value)
    {
        _si = 0;
        std::minstd_rand rd(value);
        std::uniform_int_distribution<uint64_t> uid(0ULL, 0x7fffffffffffffffULL);
        bool flag = false;
        for (int i = 0; i < k; ++i)
        {
            _state[i] = (uid(rd) << 1) | 1ULL;
            if ((_state[i] & 0x2ULL) == 0x2ULL)
            {
                flag = true;
            }
        }
        if (!flag)
        {
            _state[0] |= 0x2ULL;
        }
    }

    template<int k, int l> template<typename InputIterator>
    void mlfe<k, l>::seed(InputIterator first, InputIterator last)
    {
        assert(last - first == state_size);
        _si = 0;
        bool flag = false;
        InputIterator it = first;
        uint64_t* ptr = _state;
        while (it != last)
        {
            *ptr = (*it) | 1ULL;
            if (((*it) & 0x2ULL) == 0x2ULL)
            {
                flag = true;
            }
            ++ptr;
            ++it;
        }
        if (!flag)
        {
            _state[0] |= 0x2ULL;
        }
    }

    template<int k, int l>
    uint64_t mlfe<k, l>::operator()()
    {
        int siml = _si - l;
        if (siml < 0)
        {
            siml += k;
        }
        uint64_t tmp = _state[_si] * _state[siml];
        _state[_si] = tmp;
        ++_si;
        if (_si == k)
        {
            _si = 0;
        }
        return tmp >> 1;
    }

    template<int k, int l> template<typename OutputIterator>
    void mlfe<k, l>::get_state(OutputIterator first, OutputIterator last)
    {
        for (int j = 0; j < k; ++j)
        {
            int i = (j + _si) % k;
            *first = _state[i];
            ++first;
        }
    }
}
#endif // _WAT_MLFE_HPP
