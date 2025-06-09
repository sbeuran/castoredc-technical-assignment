import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getSortedRowModel,
  SortingState,
  getFilteredRowModel,
  ColumnDef,
} from '@tanstack/react-table';
import { useState } from 'react';
import { MoreVertical } from 'lucide-react';

interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
}

const StatusBadge = ({ status }: { status: string }) => {
  const getStatusStyles = (status: string) => {
    switch (status) {
      case 'processed':
        return 'bg-green-500/20 text-green-400';
      case 'to be processed':
        return 'bg-blue-500/20 text-blue-400';
      default:
        return 'bg-gray-500/20 text-gray-400';
    }
  };

  return (
    <span className={`px-2 py-1 rounded-md text-xs font-medium ${getStatusStyles(status.toLowerCase())}`}>
      {status}
    </span>
  );
};

export default function DataTable<T>({ data, columns }: DataTableProps<T>) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  const toggleAllRows = () => {
    if (selectedRows.size === table.getRowModel().rows.length) {
      setSelectedRows(new Set());
    } else {
      setSelectedRows(new Set(table.getRowModel().rows.map(row => row.id)));
    }
  };

  const toggleRow = (rowId: string) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(rowId)) {
      newSelected.delete(rowId);
    } else {
      newSelected.add(rowId);
    }
    setSelectedRows(newSelected);
  };

  return (
    <div className="w-full bg-[#0A0F1C] rounded-xl overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-800/60">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-200">
            Orders
            <span className="ml-2 text-sm font-normal text-gray-400">
              ({table.getFilteredRowModel().rows.length} total)
            </span>
          </h2>
          <div className="text-sm text-gray-400">
            {selectedRows.size} selected
          </div>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-separate border-spacing-0">
          <thead>
            <tr>
              <th className="sticky top-0 text-left py-3 px-4 bg-[#0D1425] border-b border-gray-800/60">
                <input
                  type="checkbox"
                  checked={selectedRows.size === table.getRowModel().rows.length}
                  onChange={toggleAllRows}
                  className="rounded border-gray-600 bg-transparent cursor-pointer
                    focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </th>
              {table.getHeaderGroups().map((headerGroup) => (
                headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    onClick={header.column.getToggleSortingHandler()}
                    className="sticky top-0 text-left py-3 px-4 text-xs font-medium text-gray-400 
                      bg-[#0D1425] border-b border-gray-800/60 uppercase tracking-wider cursor-pointer
                      hover:text-gray-200 transition-colors"
                  >
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))
              ))}
              <th className="sticky top-0 w-10 py-3 px-4 bg-[#0D1425] border-b border-gray-800/60"></th>
            </tr>
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr 
                key={row.id}
                className="group hover:bg-gray-800/30 transition-colors duration-150"
              >
                <td className="py-3 px-4">
                  <input
                    type="checkbox"
                    checked={selectedRows.has(row.id)}
                    onChange={() => toggleRow(row.id)}
                    className="rounded border-gray-600 bg-transparent cursor-pointer
                      focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </td>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="py-3 px-4 text-sm text-gray-300">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
                <td className="py-3 px-4">
                  <button className="opacity-0 group-hover:opacity-100 transition-opacity duration-150
                    text-gray-400 hover:text-gray-200 focus:outline-none focus:text-gray-200">
                    <MoreVertical className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="px-6 py-4 border-t border-gray-800/60 bg-[#0D1425]">
        <div className="flex items-center justify-center gap-2">
          <button className="px-3 py-2 text-sm font-medium text-gray-400 hover:text-gray-200 
            hover:bg-gray-800/50 rounded transition-colors">
            Previous
          </button>
          <div className="flex items-center">
            {[1, 2, 3].map((page) => (
              <button
                key={page}
                className="px-3 py-2 text-sm font-medium text-gray-400 hover:text-gray-200 
                  hover:bg-gray-800/50 rounded transition-colors"
              >
                {page}
              </button>
            ))}
            <span className="px-2 text-gray-600">...</span>
            <button className="px-3 py-2 text-sm font-medium text-gray-400 hover:text-gray-200 
              hover:bg-gray-800/50 rounded transition-colors">
              37
            </button>
          </div>
          <button className="px-3 py-2 text-sm font-medium text-gray-400 hover:text-gray-200 
            hover:bg-gray-800/50 rounded transition-colors">
            Next
          </button>
        </div>
      </div>
    </div>
  );
} 