from django.shortcuts import render
import csv
import io
import pandas as pd
import numpy as np
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CSVUploadSerializer

def infer_and_convert_data_types(df):
    for col in df.columns:
        # Convert boolean columns
        if df[col].dropna().isin([True, False]).all():
            df[col] = df[col].astype(bool)
            continue

        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')

        if not df_converted.isna().all():  # If at least one value is numeric
            if all(isinstance(x, int) for x in df_converted.dropna()):
                if np.iinfo(np.int8).min <= df_converted.min() and df_converted.max() <= np.iinfo(np.int8).max:
                    df[col] = df_converted.astype('int8')
                elif np.iinfo(np.int16).min <= df_converted.min() and df_converted.max() <= np.iinfo(np.int16).max:
                    df[col] = df_converted.astype('int16')
                elif np.iinfo(np.int32).min <= df_converted.min() and df_converted.max() <= np.iinfo(np.int32).max:
                    df[col] = df_converted.astype('int32')
                elif np.iinfo(np.int64).min <= df_converted.min() and df_converted.max() <= np.iinfo(np.int64).max:
                    df[col] = df_converted.astype('int64')
            elif all(isinstance(x, float) for x in df_converted.dropna()):
                # Check for float32 range
                if np.finfo(np.float32).min <= df_converted.min() and df_converted.max() <= np.finfo(np.float32).max:
                    df[col] = df_converted.astype('float32')
                # Check for float64 range
                elif np.finfo(np.float64).min <= df_converted.min() and df_converted.max() <= np.finfo(np.float64).max:
                    df[col] = df_converted.astype('float64')
            else:
                df[col] = df_converted
            continue

        # Attempt to convert to datetime
        try:
            df[col] = pd.to_datetime(df[col])
            continue
        except (ValueError, TypeError):
            pass

        # Attempt to convert to timedelta
        try:
            df[col] = pd.to_timedelta(df[col])
            continue
        except (ValueError, TypeError):
            pass

        # Attempt to convert to complex numbers
        try:
            df[col] = df[col].apply(lambda x: complex(x))
            continue
        except (ValueError, TypeError):
            pass

        # Check if the column should be categorical
        if len(df[col].unique()) / len(df[col]) < 0.7:
            df[col] = pd.Categorical(df[col])
            continue

        # Convert to object (if none of the above types match)
        df[col] = df[col].astype(object)

    return df
    
class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            data_set = file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)

            try:
                df = pd.read_csv(io_string)
                dtypes_before = df.dtypes.astype(str).to_dict() # Data types before conversion 
                df = infer_and_convert_data_types(df) 
                dtypes_after = df.dtypes.astype(str).to_dict() # Data types after conversion
                first_two_lines = df.head(2).to_dict(orient='records')
                response_data = { 
                    'dtypes_before': dtypes_before, 
                    'dtypes_after': dtypes_after,
                    'first_two_lines': first_two_lines
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

