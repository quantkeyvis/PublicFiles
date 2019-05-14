# Device DGA API

## Usage


## Lookup site labels

"GET /device/'<'DGA_Ind: identifier'>'"

**Arguments**

-'identifier':string a website string



**Response**

- '404 Not Found
''' json
{'message': 'Error in classification: number somehow passed', 
'data': 'N/A'}
'''

- '200 OK' on success

''' json
{
"data":"classification"
"message": "tells you what happend"
}
'''

