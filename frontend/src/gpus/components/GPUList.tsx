import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GPUComparisonTable from './GPUComparisonTable';
import { gpuModelComparator } from '../gpuModelComparator';
import { GPU, Store, GPUComparison } from '../types/interfaces';

const GPUList: React.FC = () => {
  const [gpuComparisonsNvidia, setGpuComparisonsNvidia] = useState<GPUComparison[]>([]);
  const [gpuComparisonsAMD, setGpuComparisonsAMD] = useState<GPUComparison[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [gpusResponse, storesResponse] = await Promise.all([
          axios.get<GPU[]>('http://localhost:8000/gpus'),
          axios.get<Store[]>('http://localhost:8000/stores'),
        ]);

        const gpus = gpusResponse.data;
        const stores = storesResponse.data;

        setStores(stores);

        // Process the data
        const comparisonsNvidia: { [key: string]: GPUComparison } = {};
        const comparisonsAMD: { [key: string]: GPUComparison } = {};

        gpus.forEach(gpu => {
          if (!gpu.model || !gpu.price || !gpu.store) return; // Skip incomplete data

          const brand = gpu.brand ? gpu.brand.trim().toLowerCase() : '';

          let comparisons = null;
          if (brand === 'nvidia') {
            comparisons = comparisonsNvidia;
          } else if (brand === 'amd') {
            comparisons = comparisonsAMD;
          } else {
            return; // Skip unknown brands
          }

          const modelKey = gpu.model.trim().toLowerCase();

          if (!comparisons[modelKey]) {
            comparisons[modelKey] = {
              model: gpu.model.trim(), // Original model name
              prices: {},
              gpus: [],
              benchmark_score: gpu.benchmark_score || null,
            };
          }

          comparisons[modelKey].gpus.push(gpu);

          const storeName = gpu.store.trim();
          const currentPrice = comparisons[modelKey].prices[storeName];
          if (!currentPrice || parseFloat(gpu.price) < parseFloat(currentPrice)) {
            comparisons[modelKey].prices[storeName] = gpu.price;
          }
        });

        // Sort the GPU models logically
        const sortGPUComparisons = (comparisons: GPUComparison[]) => {
          return comparisons.sort((a, b) => {
            return gpuModelComparator(a.model, b.model);
          });
        };

        setGpuComparisonsNvidia(sortGPUComparisons(Object.values(comparisonsNvidia)));
        setGpuComparisonsAMD(sortGPUComparisons(Object.values(comparisonsAMD)));

        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(`Failed to fetch data: ${err instanceof Error ? err.message : 'Unknown error'}`);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="text-center mt-8 text-gray-300">Loading...</div>;
  if (error) return <div className="text-center mt-8 text-red-400">Error: {error}</div>;

  return (
    <div className="gpus-container w-full">
      <h1 className="text-3xl font-bold mb-8 text-center text-gray-100">GPU Price Comparison</h1>
      <GPUComparisonTable
        gpuComparisons={gpuComparisonsNvidia}
        title="NVIDIA GPUs"
        stores={stores}
      />
      <GPUComparisonTable
        gpuComparisons={gpuComparisonsAMD}
        title="AMD GPUs"
        stores={stores}
      />
    </div>
  );
};

export default GPUList;
