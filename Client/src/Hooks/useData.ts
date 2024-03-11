import { useEffect, useState } from "react";
import apiClient from "../services/apiClient";
import { AxiosError, AxiosRequestConfig } from "axios";

export interface date {
  date: number;
  hour: number;
  minute: number;
  month: number;
  second: number;
  year: number;
}

export interface detection {
  day: date;
  number_plate: string;
}

export const useData = <T>(
  endPoint: string,
  toggle: boolean,
  requestConfig?: AxiosRequestConfig
) => {
  const [Data, setData] = useState<T>();

  const [err, setErr] = useState<string>();

  useEffect(() => {
    // const abortController = new AbortController();
    apiClient
      .get<T>(endPoint, {
        // signal: abortController.signal,
        ...requestConfig,
      })
      .then((response) => {
        console.log("Response received:", response.data);
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error occurred:", error);
        setErr(error.message || "An error occurred");
      });
  }, [toggle]);

  return { Data, err };
};
