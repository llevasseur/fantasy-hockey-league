import "./ServerStatus.scss";
import { useState, useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;
// const API_URL = import.meta.env.VITE_DEV_API_URL;

const ServerStatus = () => {
  const [status, setStatus] = useState("");
  const location = useLocation().pathname;
  const params = useParams();

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}` + location, {
          headers: {
            "Content-Type": "application/json",
          },
        });
        setStatus(response.data);
      } catch (error) {
        console.error("Error fetching status");
        setStatus("Game 7 OT loss to Server");
      }
    };
    fetchStatus();
  }, []);

  return <h4 className="server-status">Server Status: {status}</h4>;
};

export default ServerStatus;
