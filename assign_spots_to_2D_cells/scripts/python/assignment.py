from aicsimageio import AICSImage
import pandas as pd
import anndata
import fire


VERSION = "0.0.1"

def main(label_image, transcripts, out_name, pixelsize=1):
    print('Reading image and transcripts')
    if transcripts.endswith('.csv'):
        spots = pd.read_csv(transcripts, header=0, sep=',')[['y_location', 'x_location', 'feature_name']]
    elif transcripts.endswith('.tsv'):
        spots = pd.read_csv(transcripts, header=0, sep='\t')[['y_location', 'x_location', 'feature_name']]
    elif transcripts.endswith('.wkt'):
        from shapely import from_wkt, MultiPoint
        # Assuming that the wkt file contains a multipoint geometry
        with open(transcripts, 'r') as f:
            multispots = from_wkt(f.read())
        if not isinstance(multispots, MultiPoint):
            raise ValueError('Please provide a wkt file with multipoint geometry')
        spots = pd.DataFrame([(geom.y, geom.x) for geom in multispots.geoms], columns=['y_location', 'x_location'])
        spots["feature_name"] = 'spot'
    else:
        raise ValueError('Format not recognized. Please provide a csv, tsv or wkt file')
    lab_2D = AICSImage(label_image)

    print('Performing assignment')
    cell_id = lab_2D.dask_data[spots["y_location"].astype(int)/pixelsize, spots["x_location"].astype(int)/pixelsize]
    spots['cell_id'] = cell_id
    count_matrix = spots.pivot_table(index='cell_id', columns='feature_name', aggfunc='size', fill_value=0)
    count_matrix = count_matrix.drop(count_matrix[count_matrix.index == 0].index)
    count_matrix.to_csv(out_name)
        
    
if __name__ == "__main__":
    options = {
        "run": main,
        "version": VERSION
    }
    fire.Fire(options)
        
    
