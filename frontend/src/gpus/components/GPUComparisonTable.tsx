import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from "../../components/ui/table";
import ExpandableTableRow from './ExpandableTableRow';
import { Store, GPUComparison } from '../types/interfaces';

interface GPUComparisonTableProps {
  gpuComparisons: GPUComparison[];
  title: string;
  stores: Store[];
}

const GPUComparisonTable: React.FC<GPUComparisonTableProps> = ({ gpuComparisons, title, stores }) => {
  const [expandedModel, setExpandedModel] = useState<string | null>(null);

  return (
    <div className="my-8 w-full bg-gray-900">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-100">{title}</h2>
      <div className="overflow-x-auto">
        <Table className="w-full">
          <TableHeader>
            <TableRow>
              <TableHead className="w-1/4 text-gray-200">Model</TableHead>
              {stores.map(store => (
                <TableHead key={store.name} className="w-1/6 text-center text-gray-200">
                  <div className="flex justify-center items-center h-full">
                    <a 
                      href={store.store_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-block"
                    >
                      <img 
                        src={store.logo_url} 
                        alt={store.name} 
                        title={store.name}
                        className="h-6 mb-2"
                      />
                    </a>
                  </div>
                </TableHead>
              ))}
              <TableHead className="w-1/6 text-center">PassMark - G3D Mark</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {gpuComparisons.map(comparison => (
              <ExpandableTableRow
                key={comparison.model}
                comparison={comparison}
                stores={stores}
                expandedModel={expandedModel}
                setExpandedModel={setExpandedModel}
              />
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default GPUComparisonTable;