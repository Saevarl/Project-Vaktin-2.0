import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../../components/ui/table";
import { GPU, Store } from '../types/interfaces';



interface GPUDetailsTableProps {
  gpus: GPU[];
  stores: Store[];
}

const formatPrice = (price: string): string => {
  return `${parseFloat(price).toLocaleString('is-IS', { minimumFractionDigits: 3, maximumFractionDigits: 3 })}kr`;
};


const GPUDetailsTable: React.FC<GPUDetailsTableProps> = ({ gpus, stores }) => {
  const formatPrice = (price: string): string => {
    return `${parseFloat(price).toLocaleString('is-IS', { minimumFractionDigits: 3, maximumFractionDigits: 3 })}kr`;
  };

  const handlePriceClick = (e: React.MouseEvent, link: string) => {
    e.stopPropagation();
    window.open(link, '_blank');
  };

  return (
    <div className="bg-gray-800 rounded-lg mt-4 p-4">
      <Table className="w-full">
        <TableHeader>
          <TableRow>
            <TableHead className="w-1/2 text-gray-200">Model</TableHead>
            {stores.map(store => (
              <TableHead key={store.name} className="w-1/4 text-center">
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
          </TableRow>
        </TableHeader>
        <TableBody>
          {gpus
            .sort((a, b) => parseFloat(a.price) - parseFloat(b.price))
            .map((gpu) => (
              <TableRow key={gpu.link} className="hover:bg-gray-700">
                <TableCell className="w-1/2">
                  <a 
                    href={gpu.link} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="text-gray-300 hover:text-gray-100 hover:underline transition-colors duration-200 inline-block"
                    title={gpu.name}
                  >
                    {gpu.name}
                  </a>
                </TableCell>
                {stores.map(store => (
                  <TableCell key={store.name} className="w-1/4 text-center text-gray-300">
                    {store.name === gpu.store ? (
                      <span 
                        className="cursor-pointer hover:underline"
                        onClick={(e) => handlePriceClick(e, gpu.link)}
                      >
                        {formatPrice(gpu.price)}
                      </span>
                    ) : '-'}
                  </TableCell>
                ))}
              </TableRow>
            ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default GPUDetailsTable;