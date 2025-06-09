'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import { 
  DataGrid, 
  GridColDef, 
  GridActionsCellItem,
  GridRenderCellParams,
  GridToolbar
} from '@mui/x-data-grid';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import DeleteOutlineOutlinedIcon from '@mui/icons-material/DeleteOutlineOutlined';
import RefreshIcon from '@mui/icons-material/RefreshOutlined';
import FileDownloadIcon from '@mui/icons-material/FileDownloadOutlined';
import ListAltOutlinedIcon from '@mui/icons-material/ListAltOutlined';
import DataArrayIcon from '@mui/icons-material/DataArrayOutlined';
import ExtendedDataView from '@/components/ExtendedDataView';

// Types
interface BasicFruit {
  id: number;
  fruit: string;
  color: string;
}

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

interface AllData {
  fruits: ExtendedFruit[];
  total_fruits: number;
  total_suppliers: number;
  total_nutritional_records: number;
}

// Create a dark theme
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
});

export default function Home() {
  const [basicFruits, setBasicFruits] = useState<BasicFruit[]>([]);
  const [allData, setAllData] = useState<AllData | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'list' | 'extended'>('list');

  const API_BASE_URL = 'https://fruits-api-app.azurewebsites.net/api/v1';

  useEffect(() => {
    fetchBasicFruits();
  }, []);

  useEffect(() => {
    if (activeTab === 'extended') {
      fetchAllData();
    }
  }, [activeTab]);

  const fetchBasicFruits = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/fruits`);
      setBasicFruits(response.data);
      toast.success('Fruits loaded successfully');
    } catch (error) {
      toast.error('Failed to load fruits');
      console.error('Error fetching fruits:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/get_all_data`);
      console.log('Fetched data:', response.data);
      if (!response.data || !response.data.fruits || !Array.isArray(response.data.fruits)) {
        throw new Error('Invalid data format received');
      }
      setAllData(response.data);
      toast.success('All data loaded successfully');
    } catch (error) {
      console.error('Error fetching all data:', error);
      toast.error('Failed to load all data');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (id: number) => {
    console.log('Edit fruit:', id);
    // Add edit logic here
  };

  const handleDelete = (id: number) => {
    console.log('Delete fruit:', id);
    // Add delete logic here
  };

  const columns: GridColDef[] = [
    {
      field: 'fruit',
      headerName: 'Fruit Name',
      flex: 1,
      renderCell: (params) => (
        <div className="flex items-center">
          <span 
            className="w-2 h-2 rounded-full mr-3" 
            style={{ backgroundColor: params.row.color }} 
          />
          <span className="font-medium capitalize">
            {params.value}
          </span>
        </div>
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 100,
      type: 'actions',
      getActions: (params) => [
        <GridActionsCellItem
          key="edit"
          icon={<EditOutlinedIcon />}
          label="Edit"
          onClick={() => handleEdit(params.row.id)}
          showInMenu={false}
        />,
        <GridActionsCellItem
          key="delete"
          icon={<DeleteOutlineOutlinedIcon />}
          label="Delete"
          onClick={() => handleDelete(params.row.id)}
          showInMenu={false}
        />,
      ],
    },
  ];

  const renderTabs = () => (
    <div className="flex space-x-1 rounded-xl bg-[#242b4a] p-1 mb-6">
      <button
        onClick={() => setActiveTab('list')}
        className={`w-full rounded-lg py-2.5 text-sm font-medium leading-5 flex items-center justify-center gap-2 transition-all duration-200
          ${activeTab === 'list' 
            ? 'bg-white text-blue-600 shadow' 
            : 'text-gray-400 hover:bg-white/[0.12] hover:text-white'}`}
      >
        <ListAltOutlinedIcon sx={{ fontSize: 20 }} />
        List Fruits
      </button>
      <button
        onClick={() => setActiveTab('extended')}
        className={`w-full rounded-lg py-2.5 text-sm font-medium leading-5 flex items-center justify-center gap-2 transition-all duration-200
          ${activeTab === 'extended' 
            ? 'bg-white text-blue-600 shadow' 
            : 'text-gray-400 hover:bg-white/[0.12] hover:text-white'}`}
      >
        <DataArrayIcon sx={{ fontSize: 20 }} />
        Extended Data
      </button>
    </div>
  );

  const renderBasicFruits = () => (
    <div className="animate-fadeIn">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Fruits ({basicFruits.length} total)</h2>
        <div className="flex gap-2">
          <button
            onClick={fetchBasicFruits}
            disabled={loading}
            className="inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors
              bg-blue-500 text-white hover:bg-blue-600 disabled:opacity-50"
          >
            <RefreshIcon className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>
      </div>
      <div style={{ height: 400, width: '100%' }}>
        <ThemeProvider theme={darkTheme}>
          <DataGrid
            rows={basicFruits}
            columns={columns}
            loading={loading}
            disableRowSelectionOnClick
            slots={{ toolbar: GridToolbar }}
            slotProps={{
              toolbar: {
                showQuickFilter: true,
                quickFilterProps: { debounceMs: 500 },
              },
            }}
            pageSizeOptions={[5, 10, 25]}
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
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                padding: '8px 16px',
                borderRadius: '4px',
              },
              '& .MuiButton-root': {
                color: 'rgba(255, 255, 255, 0.7)',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                },
              },
            }}
          />
        </ThemeProvider>
      </div>
    </div>
  );

  const renderExtendedData = () => (
    <div className="animate-fadeIn">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Extended Data</h2>
        <div className="flex gap-2">
          <button
            onClick={fetchAllData}
            disabled={loading}
            className="inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors
              bg-blue-500 text-white hover:bg-blue-600 disabled:opacity-50"
          >
            <RefreshIcon className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>
      </div>
      {loading && !allData && (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      )}
      {allData && allData.fruits && allData.fruits.length > 0 ? (
        <div className="space-y-6">
          <ExtendedDataView data={allData.fruits} />
        </div>
      ) : (
        !loading && (
          <div className="flex items-center justify-center h-64 text-gray-400">
            No data available. Click refresh to load data.
          </div>
        )
      )}
    </div>
  );

  return (
    <div>
      {renderTabs()}
      {activeTab === 'list' && renderBasicFruits()}
      {activeTab === 'extended' && renderExtendedData()}
    </div>
  );
} 