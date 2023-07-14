import java.util.HashMap;
import java.util.ArrayList;

public class Dataframe
{
	ArrayList<String> headers;
	HashMap<String, ArrayList<String>> map;
	int size;

	public Dataframe(ArrayList<String> headers, HashMap<String, ArrayList<String>> map)
	{
		this.headers = headers;
		this.map = map;
		// number of rows
		this.size = map.get(headers.get(0)).size();		
	}

	public int size()
	{
		return(size);
	}

	// get methods -------------------------------------
	private ArrayList<String> getColumn(String header)
	{
		if(!(headers.contains(header)))
		{
			return null;
		}

		ArrayList<String> column = map.get(header);
		return column;
	}

	private ArrayList<String> getRow(int number)
	{
		if(number >= size) return null;
		if(number < 0) return null;

		ArrayList<String> row = new ArrayList<String>();
		// use headers to ensure that order is maintained
		for(String field : headers) 
		{
			String rowElement = map.get(field).get(number);
			row.add(rowElement);
		}
		return row;
	}

	public ArrayList<String> get(String header)
	{
		return getColumn(header);
	}

	public ArrayList<String> get(int number)
	{
		return getRow(number);
	}
	// ------------------------------------------------
	
	// split by column (separate into 2 dataframes)
	public Dataframe split(String startColumn, String endColumn)
	{
		if(!(headers.contains(startColumn))) return null;
		if(!(headers.contains(endColumn))) return null;

		int startIndex = headers.indexOf(startColumn);
		int endIndex = headers.indexOf(endColumn);

		ArrayList<String> newHeaders = new ArrayList<String>();
		HashMap<String, ArrayList<String>> newMap = new HashMap<String, ArrayList<String>>();
		for(int i = startIndex; i <= endIndex; i++)
		{
			String header = headers.get(i);
			newHeaders.add(header);
			newMap.put(header, new ArrayList<String>());
		}

		for(int i = 0; i < size; i++)
		{
			for(String header : newHeaders)
			{
				String element = map.get(header).get(i);
				newMap.get(header).add(element);
			}
		}
		Dataframe newDataframe = new Dataframe(newHeaders, newMap);
		return newDataframe;
	}
	//----------------------------------------------------
	
	// Printing the dataframe
	public int getColumnWidth(String columnName)
	{
		if(!(headers.contains(columnName)))
		{
			return -1;
		}

		ArrayList<String> column = map.get(columnName);
		int columnSize = column.size() + 1; // plus one to account for header 
		int[] lengths = new int[columnSize];
		int width = -1;
		for(int i = 0; i < columnSize - 1; i++)
		{
			lengths[i] = column.get(i).length();
			if(lengths[i] > width) width = lengths[i];
		}

		int headerLength = columnName.length();
		lengths[columnSize-1] = headerLength;
		if(headerLength > width) width = headerLength;

		return width;
	}

	public int[] getColumnWidths()
	{
		int cardinality = headers.size();
		int[] widths = new int[cardinality];
		for(int i = 0; i < cardinality; i++)
		{
			String header = headers.get(i);
			widths[i] = getColumnWidth(header);
		}
		return widths;
	}
} 
