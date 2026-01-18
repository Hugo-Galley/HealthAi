import pandas as pd

class DataCleaning:
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        return(
            df
            .drop_duplicates(keep="last")
            .reset_index(drop=True)
        )