import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface GPU {
  name: string;
  link: string;
  model: string;
  price: string;
  store: string;
  manufacturer: string;
  date_checked: string;
  brand: string;
  series: string;
  vram: number;
}

interface GPUComparison {
  model: string;
  kisildalur: string | null;
  tolvutaekni: string | null;
  gpus: GPU[];
}

const GPUs: React.FC = () => {
  const [gpuComparisons, setGpuComparisons] = useState<GPUComparison[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedModel, setExpandedModel] = useState<string | null>(null);

  useEffect(() => {
    const fetchGPUs = async () => {
      try {
        const response = await axios.get<GPU[]>('http://localhost:8000/gpus');
        const gpus = response.data;
        
        // Process the data
        const comparisons: { [key: string]: GPUComparison } = {};
        
        gpus.forEach(gpu => {
          if (!comparisons[gpu.model]) {
            comparisons[gpu.model] = {
              model: gpu.model,
              kisildalur: null,
              tolvutaekni: null,
              gpus: []
            };
          }
          
          comparisons[gpu.model].gpus.push(gpu);
          
          if (gpu.store === 'Kisildalur' && (!comparisons[gpu.model].kisildalur || parseFloat(gpu.price) < parseFloat(comparisons[gpu.model].kisildalur!))) {
            comparisons[gpu.model].kisildalur = gpu.price;
          }
          
          if (gpu.store === 'Tölvutækni' && (!comparisons[gpu.model].tolvutaekni || parseFloat(gpu.price) < parseFloat(comparisons[gpu.model].tolvutaekni!))) {
            comparisons[gpu.model].tolvutaekni = gpu.price;
          }
        });
        
        setGpuComparisons(Object.values(comparisons));
        setLoading(false);
      } catch (err) {
        console.error('Error fetching GPUs:', err);
        setError(`Failed to fetch GPUs: ${err instanceof Error ? err.message : 'Unknown error'}`);
        setLoading(false);
      }
    };

    fetchGPUs();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="gpus-container">
      <h1>GPU Price Comparison</h1>
      <table className="gpu-table">
        <thead>
          <tr>
            <th>Model</th>
            <th>Kísildalur</th>
            <th>Tölvutækni</th>
          </tr>
        </thead>
        <tbody>
          {gpuComparisons.map((comparison) => (
            <React.Fragment key={comparison.model}>
              <tr onClick={() => setExpandedModel(expandedModel === comparison.model ? null : comparison.model)}>
                <td>{comparison.model}</td>
                <td>{comparison.kisildalur || 'N/A'}</td>
                <td>{comparison.tolvutaekni || 'N/A'}</td>
              </tr>
              {expandedModel === comparison.model && (
                <tr>
                  <td colSpan={3}>
                    <table className="expanded-gpu-table">
                      <thead>
                        <tr>
                          <th>Name</th>
                          <th>Store</th>
                          <th>Price</th>
                        </tr>
                      </thead>
                      <tbody>
                        {comparison.gpus
                          .sort((a, b) => parseFloat(a.price) - parseFloat(b.price))
                          .map((gpu, index) => (
                            <tr key={index}>
                              <td>{gpu.name}</td>
                              <td>{gpu.store}</td>
                              <td>{gpu.price}</td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default GPUs;