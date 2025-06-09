'use client';

import { useMemo } from 'react';
import { 
  DataGrid, 
  GridColDef,
  GridRenderCellParams,
  GridToolbar
} from '@mui/x-data-grid';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Image from 'next/image';
import Tooltip from '@mui/material/Tooltip';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarHalfIcon from '@mui/icons-material/StarHalf';
import * as flags from 'country-flag-icons/react/3x2';

interface ExtendedFruit {
  id: number;
  name: string;
  color: string;
  taste: string;
  origin_country: string;
  price_per_kg: number;
  status: string;
  created_at: string;
  nutritional_info: {
    calories: number;
    carbohydrates: number;
    protein: number;
    fat: number;
    fiber: number;
    vitamins: string;
  };
  suppliers: Array<{
    id: number;
    name: string;
    contact_email: string;
    country: string;
    rating: number;
  }>;
}

interface ExtendedDataViewProps {
  data: ExtendedFruit[];
}

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    background: {
      default: '#0A0F1C',
      paper: '#1a1f35',
    },
    primary: {
      main: '#3b82f6',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#0A0F1C',
        },
      },
    },
  },
});

const CountryFlag = ({ country }: { country: string }) => {
  const countryToCode: { [key: string]: string } = {
    'USA': 'US',
    'Spain': 'ES',
    'Ecuador': 'EC',
    // Add more mappings as needed
  };

  const code = countryToCode[country] || country;
  const FlagComponent = (flags as any)[code];

  if (!FlagComponent) {
    return <span className="text-xs text-gray-400">{country}</span>;
  }

  return (
    <div className="flex flex-col items-start gap-1">
      <div className="w-6 h-4">
        <FlagComponent title={country} />
      </div>
      <span className="text-xs text-gray-400">{country}</span>
    </div>
  );
};

const RatingStars = ({ rating }: { rating: number }) => {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
  
  return (
    <div className="flex items-center text-yellow-400">
      {[...Array(fullStars)].map((_, i) => (
        <StarIcon key={`full-${i}`} sx={{ fontSize: 16 }} />
      ))}
      {hasHalfStar && <StarHalfIcon sx={{ fontSize: 16 }} />}
      {[...Array(emptyStars)].map((_, i) => (
        <StarBorderIcon key={`empty-${i}`} sx={{ fontSize: 16 }} />
      ))}
      <span className="ml-1 text-sm text-gray-400">{rating.toFixed(1)}</span>
    </div>
  );
};

const NutritionTooltip = ({ info }: { info: ExtendedFruit['nutritional_info'] }) => (
  <div className="p-2">
    <div>Protein: {info.protein}g</div>
    <div>Fat: {info.fat}g</div>
    <div>Fiber: {info.fiber}g</div>
    <div>Vitamins: {info.vitamins}</div>
  </div>
);

const SupplierTooltip = ({ supplier }: { supplier: ExtendedFruit['suppliers'][0] }) => (
  <div className="p-2">
    <div>Rating: {supplier.rating}/5</div>
    <div>Email: {supplier.contact_email}</div>
    <div>Country: {supplier.country}</div>
  </div>
);

export default function ExtendedDataView({ data }: ExtendedDataViewProps) {
  const columns: GridColDef[] = [
    {
      field: 'id',
      headerName: '#',
      width: 70,
    },
    {
      field: 'name',
      headerName: 'Fruit Name',
      width: 130,
      renderCell: (params) => (
        <div className="flex items-center">
          <span className="w-2 h-2 rounded-full mr-3" style={{ backgroundColor: params.row.color }} />
          <span className="font-medium">{params.value}</span>
        </div>
      ),
    },
    {
      field: 'origin_country',
      headerName: 'Origin',
      width: 120,
      renderCell: (params: GridRenderCellParams<ExtendedFruit>) => (
        <CountryFlag country={params.value as string} />
      ),
      valueGetter: (params) => params.value,
    },
    {
      field: 'taste',
      headerName: 'Taste',
      width: 120,
    },
    {
      field: 'nutritional_info',
      headerName: 'Nutrition',
      width: 180,
      valueGetter: (params) => {
        const info = params.row.nutritional_info;
        return `${info.calories}cal, ${info.carbohydrates}g carbs, ${info.protein}g protein, ${info.fat}g fat, ${info.fiber}g fiber, Vitamins: ${info.vitamins}`;
      },
      renderCell: (params) => {
        const info = params.row.nutritional_info;
        return (
          <Tooltip 
            title={<NutritionTooltip info={info} />}
            placement="right"
          >
            <div className="flex items-center gap-2">
              <span className="text-gray-300">
                {info.calories} cal | {info.carbohydrates}g carbs
              </span>
              <InfoOutlinedIcon className="text-gray-500" sx={{ fontSize: 16 }} />
            </div>
          </Tooltip>
        );
      },
    },
    {
      field: 'suppliers',
      headerName: 'Supplier',
      width: 180,
      valueGetter: (params) => {
        const supplier = params.row.suppliers[0];
        return `${supplier.name} (${supplier.rating}/5) - ${supplier.contact_email} - ${supplier.country}`;
      },
      renderCell: (params) => {
        const supplier = params.row.suppliers[0];
        return (
          <Tooltip 
            title={<SupplierTooltip supplier={supplier} />}
            placement="right"
          >
            <div className="flex items-center gap-2">
              <span className="text-gray-300">{supplier.name}</span>
              <InfoOutlinedIcon className="text-gray-500" sx={{ fontSize: 16 }} />
            </div>
          </Tooltip>
        );
      },
    },
    {
      field: 'created_at',
      headerName: 'Date Added',
      width: 180,
      valueGetter: (params) => {
        return params.value ? new Date(params.value).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }) : '';
      },
    },
  ];

  const processedData = useMemo(() => {
    return data.map(fruit => ({
      ...fruit,
      created_at: new Date().toISOString()
    }));
  }, [data]);

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <div style={{ height: 600, width: '100%' }} className="animate-fadeIn">
        <DataGrid
          rows={processedData}
          columns={columns}
          disableRowSelectionOnClick
          slots={{ toolbar: GridToolbar }}
          slotProps={{
            toolbar: {
              showQuickFilter: true,
              quickFilterProps: { debounceMs: 500 },
              csvOptions: { 
                fileName: 'Fruits-Extended-Data',
                delimiter: ',',
                utf8WithBom: true,
              },
            },
          }}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: { paginationModel: { pageSize: 10 } },
          }}
          sx={{
            border: 'none',
            '& .MuiDataGrid-cell': {
              borderColor: 'rgba(255, 255, 255, 0.1)',
            },
            '& .MuiDataGrid-columnHeaders': {
              borderColor: 'rgba(255, 255, 255, 0.1)',
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
            },
            '& .MuiDataGrid-row:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
            },
            '& .MuiDataGrid-toolbarContainer': {
              gap: 2,
              mb: 2,
              padding: '8px 16px',
              borderRadius: '4px',
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
              '& .MuiButton-root': {
                color: 'rgba(255, 255, 255, 0.7)',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                },
                '&[aria-label="Export"]': {
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  '&:hover': {
                    backgroundColor: '#2563eb',
                  },
                },
              },
            },
          }}
        />
      </div>
    </ThemeProvider>
  );
} 