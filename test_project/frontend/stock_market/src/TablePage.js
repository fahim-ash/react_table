import { useEffect, useState, useCallback } from "react";
import { DataGrid } from "@mui/x-data-grid";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import axios from "axios";

const useFakeMutation = () => {
  return useCallback(
    (user) =>
      new Promise((resolve, reject) => {
        setTimeout(() => {
          if (user.name?.trim() === "") {
            reject(new Error("Error while saving user: name cannot be empty."));
          } else {
            resolve({ ...user, name: user.name?.toUpperCase() });
          }
        }, 200);
      }),
    []
  );
};

export default function ServerSidePersistence() {
  const mutateRow = useFakeMutation();
  const [snackbar, setSnackbar] = useState(null);
  const [data, setData] = useState([]);
  const handleCloseSnackbar = () => setSnackbar(null);

  // use this to update data in the backend , still not prpared
  const processRowUpdate = useCallback(
    async (newRow) => {
      // Make the HTTP request to save in the backend
      const response = await mutateRow(newRow);
      setSnackbar({ children: "User successfully saved", severity: "success" });
      return response;
    },
    [mutateRow]
  );

  // handle any error during updating data
  const handleProcessRowUpdateError = useCallback((error) => {
    setSnackbar({ children: error.message, severity: "error" });
  }, []);

  // get data from backend
  useEffect(() => {
    const getRowData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/stock_market");
        console.log(response.data);
        setData(response.data);
      } catch (error) {
        console.log("why");
      }
    };
    getRowData();
  }, []);

  return (
    <div style={{ height: 400, width: "100%" }}>
      <DataGrid
        rows={data}
        columns={columns}
        processRowUpdate={processRowUpdate}
        onProcessRowUpdateError={handleProcessRowUpdateError}
      />
      {!!snackbar && (
        <Snackbar
          open
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
          onClose={handleCloseSnackbar}
          autoHideDuration={6000}
        >
          <Alert {...snackbar} onClose={handleCloseSnackbar} />
        </Snackbar>
      )}
    </div>
  );
}

const columns = [
  { field: "id", headerName: "ID", width: 180, editable: false },
  {
    field: "date",
    headerName: "Date",
    type: "date",
    editable: true,
    valueGetter: (value) => value && new Date(value),
  },
  {
    field: "trade_code",
    headerName: "Trade Code",
    editable: false,
    width: 200,
  },
  {
    field: "high",
    headerName: "High",
    width: 150,
    editable: true,
  },
  {
    field: "low",
    headerName: "Low",
    width: 150,
    editable: true,
  },
  {
    field: "open",
    headerName: "Open",
    width: 150,
    editable: true,
  },
  {
    field: "close",
    headerName: "Close",
    width: 150,
    editable: true,
  },
  {
    field: "volume",
    headerName: "Volume",
    width: 150,
    editable: true,
  },
];
