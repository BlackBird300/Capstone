# comparables/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .data_loader import get_data
from .Comparables_Algorithms.DTW import DTW
from .Comparables_Algorithms.Clustering import Clustering
import logging

logger = logging.getLogger(__name__)
data_DTW, data_Clustering = get_data()


@api_view(['GET'])
def get_companies(request):
    try:
        companies = data_Clustering['Name'].unique().tolist()
        return Response({"companies": companies})
    except Exception as e:
        logger.error(f"Error in getting companies: {e}")
        return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def run_dtw_api(request):
    target_company_name = request.query_params.get('target_company_name', None)
    if not target_company_name:
        return Response({"detail": "Please provide target_company_name query parameter."}, status=status.HTTP_400_BAD_REQUEST)
    variables = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    top_n = 5

    try:
        dtw_instance = DTW(data_DTW)
        target_company_row = data_DTW.loc[data_DTW['Name'] == target_company_name]
        if target_company_row.empty:
            raise ValueError(f"Company {target_company_name} not found in the dataset.")
        target_company = target_company_row['Symbol'].iloc[0]
        logger.info(f"Running DTW for target company: {target_company}")
        results = dtw_instance.find_most_similar(target_company, variables, top_n=top_n)
        return Response({
            "target_company": target_company,
            "top_n": top_n,
            "results": results
        })
    except ValueError as e:
        logger.error(f"ValueError in DTW execution: {e}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error in DTW execution: {e}")
        return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def run_clustering_api(request):
    target_company_name = request.query_params.get('target_company_name', None)
    if not target_company_name:
        return Response({"detail": "Please provide target_company_name query parameter."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        target_company_row = data_Clustering.loc[data_Clustering['Name'] == target_company_name]
        if target_company_row.empty:
            raise ValueError(f"Company {target_company_name} not found in the dataset.")
        target_company = target_company_row['Symbol'].iloc[0]

        clustering_instance = Clustering(data_Clustering)
        logger.info("Running Clustering...")
        clustered_data = clustering_instance.Clustering()

        target_cluster_kmeans = clustered_data.loc[clustered_data['Symbol'] == target_company, 'Cluster K-Means'].iloc[0]
        target_cluster_gmm = clustered_data.loc[clustered_data['Symbol'] == target_company, 'Cluster GMM'].iloc[0]

        target_sector = clustered_data.loc[clustered_data['Symbol'] == target_company, 'Sector'].iloc[0]

        similar_companies_kmeans = clustered_data[
            (clustered_data['Cluster K-Means'] == target_cluster_kmeans) &
            (clustered_data['Sector'] == target_sector)
        ]

        similar_companies_gmm = clustered_data[
            (clustered_data['Cluster GMM'] == target_cluster_gmm) &
            (clustered_data['Sector'] == target_sector)
        ]

        return Response({
            "target company": target_company_name,
            "target company symbol": target_company,
            "target sector": target_sector,
            # if the target company is the only one in the cluster, we don't have similar companies, flag it and return all companies operating in the same sector
            "similar companies Names (Using K-means)": similar_companies_kmeans[similar_companies_kmeans['Symbol'] != target_company]['Name'].tolist() if similar_companies_kmeans.shape[0] > 1 else clustered_data[clustered_data['Sector'] == target_sector]['Name'].tolist(),
            "similar companies Names (Using GMM)": similar_companies_gmm[similar_companies_gmm['Symbol'] != target_company]['Name'].tolist() if similar_companies_gmm.shape[0] > 1 else clustered_data[clustered_data['Sector'] == target_sector]['Name'].tolist()
        })
    except ValueError as e:
        logger.error(f"ValueError in Clustering execution: {e}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except IndexError:
        logger.error(f"Data for company {target_company} not found.")
        return Response({"detail": f"Data for company {target_company} not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Unexpected error in Clustering execution: {e}")
        return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   



    
