#pragma once

#include <succinct/mappable_vector.hpp>

#include "binary_freq_collection.hpp"
#include "bm25.hpp"
#include "util.hpp"
#include <math.h>

namespace ds2i {

    template <typename Scorer = bm25>
    class wand_data {
    public:
        wand_data()
        {}

        template <typename LengthsIterator>
        wand_data(LengthsIterator len_it, uint64_t num_docs,
                  binary_freq_collection const& coll)
        {
            std::vector<float> norm_lens(num_docs);
            double lens_sum = 0;
            logger() << "Reading sizes..." << std::endl;
            for (size_t i = 0; i < num_docs; ++i) {
                float len = *len_it++;
                norm_lens[i] = len;
                lens_sum += len;
            }
            float avg_len = float(lens_sum / double(num_docs));
            for (size_t i = 0; i < num_docs; ++i) {
                norm_lens[i] /= avg_len;
            }

            logger() << "Storing max weight for each list..." << std::endl;
            std::vector<float> max_term_weight;
            std::vector<float> upperbounds_offset;
            int upp_offset = 0;
            for (auto const& seq: coll) {
                int step = floor(sqrt(seq.docs.size()));
                //int step = 1;
                //int step = (seq.docs.size() == 1) ? 1 : floor(seq.docs.size()/2);
                //std::cout << seq.docs.size() << " " << step << std::endl;
                upperbounds_offset.push_back(max_term_weight.size());
                //std::cout << upperbounds_offset.size() << " " << max_term_weight.size() << std::endl;
                for (size_t i = 0; i < seq.docs.size(); i += step) {
                    float max_score = 0;
                    for (size_t j = i; j < seq.docs.size(); j++){
                        uint64_t docid = *(seq.docs.begin() + j);
                        uint64_t freq = *(seq.freqs.begin() + j);
                        //float score = Scorer::doc_term_weight(freq, norm_lens[docid]);
                        float score = freq;
                        max_score = std::max(max_score, score);
                    }
                    max_term_weight.push_back(i);
                    max_term_weight.push_back(max_score);
                }
                if ((max_term_weight.size() % 1000000) == 0) {
                    logger() << max_term_weight.size() << " list processed" << std::endl;
                }
            }
            logger() << max_term_weight.size() << " list processed" << std::endl;
            m_norm_lens.steal(norm_lens);
            m_max_term_weight.steal(max_term_weight);
            m_upperbounds_offset.steal(upperbounds_offset);
        }

        float norm_len(uint64_t doc_id) const
        {
            return m_norm_lens[doc_id];
        }

        float max_term_weight(uint64_t term_id) const
        {
            return m_max_term_weight[term_id];
        }


        std::vector<float> get_upper_bounds_vector(uint64_t term_id) const
        {
            std::vector<float> result;
            //            std::cout << term_id << " " << term_id+1 << std::endl;
            unsigned int startPos = m_upperbounds_offset[term_id];
            unsigned int endPos = ( term_id < (m_upperbounds_offset.size())-1 ) 
                        ? m_upperbounds_offset[term_id+1]
                        : m_max_term_weight.size();
            //std::cout << term_id << " " <<  m_upperbounds_offset[term_id] << " " <<  m_upperbounds_offset[term_id+1] << std::endl;
            for(int i = startPos; i < endPos; i = i + 2) {
                //std::cout << i << " inject: " << max_term_weight(i) << " " << max_term_weight(i+1)  << std::endl;
                result.push_back(max_term_weight(i));
                result.push_back(max_term_weight(i+1));
            }
            return result;
        }


        int upperbounds_offset(uint64_t term_id) const{
            return m_upperbounds_offset[term_id];
        }

        void swap(wand_data& other)
        {
            m_norm_lens.swap(other.m_norm_lens);
            m_max_term_weight.swap(other.m_max_term_weight);
            m_upperbounds_offset.swap(other.m_upperbounds_offset);
        }


        template <typename Visitor>
        void map(Visitor& visit)
        {
            visit
                (m_norm_lens, "m_norm_lens")
                (m_max_term_weight, "m_max_term_weight")
                (m_upperbounds_offset, "m_upperbounds_offset")
                ;
        }

    private:
        succinct::mapper::mappable_vector<float> m_norm_lens;
        succinct::mapper::mappable_vector<float> m_max_term_weight;
        succinct::mapper::mappable_vector<float> m_upperbounds_offset;
    };

}
