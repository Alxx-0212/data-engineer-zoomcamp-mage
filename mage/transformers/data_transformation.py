if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def transform_colname_to_snake_case(data):
    cols = list(data.columns)
    camel = []
    # check for camel case
    for colname in cols:
        length = len(colname)
        word_count = 0
        for char in colname:
            if 97<=ord(char)<=122 or char=='_':
                word_count+=1
        if word_count!=length:
            camel.append(colname)
    # create an empty dictionary for mapping the new column names
    d={}
    for colname in camel:
        idx=[]
        # search for _ position in the string
        for i in range(1,len(colname)):
            if 65<=ord(colname[i-1])<=90 and 97<=ord(colname[i])<=122:
                if i-1!=0:
                    idx.append(i-1)
            elif 97<=ord(colname[i-1])<=122 and 65<=ord(colname[i])<=90:
                idx.append(i)
        # transform the column name
        count = 0
        new = ''
        for k in idx:
            if new=='':
                new = colname[:k+count]+'_'+colname[k+count:]
            else:
                new = new[:k+count]+'_'+new[k+count:]
            count+=1
        d[colname]=new.lower()
    data.rename(columns=d,inplace=True)
    return data
  
@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    # Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
    data = data[~((data['passenger_count']==0) | (data['trip_distance']==0))]

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    #Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
    data = transform_colname_to_snake_case(data) 
    
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def passenger_count_greater_than_zero(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert all(list(output['passenger_count'].value_counts().index))>0

@test
def trip_distance_greater_than_zero(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert all(list(output['trip_distance'].value_counts().index))>0

@test
def vendor_id_exist(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert 'vendor_id' in output.columns