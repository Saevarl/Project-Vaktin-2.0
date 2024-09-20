import React from 'react';
import {
  TableRow,
  TableCell,
} from "../../components/ui/table";
import GPUDetailsTable from './GPUDetailsTable';
import { Store, GPUComparison } from '../types/interfaces';

interface ExpandableTableRowProps {
  comparison: GPUComparison;
  stores: Store[];
  expandedModel: string | null;
  setExpandedModel: React.Dispatch<React.SetStateAction<string | null>>;
}

const ExpandableTableRow: React.FC<ExpandableTableRowProps> = ({
  comparison,
  stores,
  expandedModel,
  setExpandedModel,
}) => {
  const isExpanded = expandedModel === comparison.model;

  const toggleExpand = () => {
    setExpandedModel(isExpanded ? null : comparison.model);
  };

  const formatPrice = (price: string | null): string => {
    return price ? `${parseFloat(price).toLocaleString('is-IS', { minimumFractionDigits: 3, maximumFractionDigits: 3 })}kr` : '-';
  };

  const handlePriceClick = (e: React.MouseEvent, link?: string) => {
    e.stopPropagation();
    if (link) {
      window.open(link, '_blank');
    }
  };

  return (
    <>
      <TableRow className="hover:bg-gray-800 cursor-pointer" onClick={toggleExpand}>
        <TableCell className="font-medium text-gray-200">{comparison.model}</TableCell>
        {stores.map(store => (
          <TableCell 
            key={store.name} 
            className="text-center text-gray-300"
          >
            {comparison.prices[store.name] && (
              <span 
                className="cursor-pointer hover:underline"
                onClick={(e) => handlePriceClick(e, comparison.gpus.find(gpu => gpu.store === store.name)?.link)}
              >
                {formatPrice(comparison.prices[store.name])}
              </span>
            )}
          </TableCell>
        ))}
        <TableCell className="text-center text-gray-300">
          {comparison.benchmark_score !== null ? comparison.benchmark_score.toLocaleString() : 'N/A'}
        </TableCell>
      </TableRow>
      {isExpanded && (
        <TableRow>
          <TableCell colSpan={stores.length + 2} className="bg-gray-800">
            <GPUDetailsTable gpus={comparison.gpus} stores={stores} />
          </TableCell>
        </TableRow>
      )}
    </>
  );
};

export default ExpandableTableRow;