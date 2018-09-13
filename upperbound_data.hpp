#pragma once


#include "binary_freq_collection.hpp"
#include "bm25.hpp"
#include "util.hpp"
#include <math.h>

namespace ds2i {

    template <typename Scorer = bm25>
    class upperbound_data {
    public:
        upperbound_data()
        {}

        template <typename LengthsIterator>
        upperbound_data(LengthsIterator len_it, uint64_t num_docs,
                  binary_freq_collection const& coll)
        {
            for (auto const& seq: coll) {
                float maxscore = 0;
                uint64_t maxscore_position = 0;
                for (size_t i = 0; i < seq.docs.size(); i += 1) {
                    uint64_t freq = *(seq.freqs.begin() + i);
                    if (freq > maxscore){
                        maxscore = freq;
                        maxscore_position = i;
                    }
                }
                std::cout << seq.docs.size() << "\t" << maxscore_position << std::endl;
            }
        }


    private:
        
    };

}
