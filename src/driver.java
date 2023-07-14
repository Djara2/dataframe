import java.util.HashMap;
import java.util.ArrayList;

public class driver
{
	public static void main(String[] argv)
	{
		ArrayList<String> headers = new ArrayList<String>();
		headers.add("Name");
		headers.add("Age");
		headers.add("Address");
		headers.add("Is Student");
		HashMap<String, ArrayList<String>> map = new HashMap<String, ArrayList<String>>();
		for(String header : headers)
		{
			map.put(header, new ArrayList<String>());
		}
		map.get("Name").add("Dave");
		map.get("Age").add("21");
		map.get("Address").add("The Overworld");
		map.get("Is Student").add("Y");

		map.get("Name").add("Sam");
		map.get("Age").add("22");
		map.get("Address").add("The Nether");
		map.get("Is Student").add("N");

		Dataframe df = new Dataframe(headers, map);

		// test: get column
		System.out.println("TEST: GET COLUMN");
		ArrayList<String> nameColumn = df.get("Name");
		for(String name : nameColumn)
		{
			System.out.println(name);
		}

		// test: get row
		System.out.println("\nTEST: GET ROW");	
		ArrayList<String> rowOne = df.get(0);
		for(int i = 0; i < rowOne.size(); i++)
		{
			String element = rowOne.get(i);
			System.out.print("\'" + element + "\'" + " ");
		}
		System.out.println();

		ArrayList<String> rowTwo = df.get(1);
		for(String element : rowTwo)
		{
			System.out.print("\'" + element + "\'" + " ");
		}
		System.out.println();

		// test: split dataframe
		System.out.println("\nTEST: SPLIT DATAFRAME");
		Dataframe split = df.split("Name", "Age");
		for(String field : split.headers)
		{
			System.out.println(field);
			for(String element : df.get(field))
			{
				System.out.println("\t" + element);
			}
			System.out.println();
		}

		// test: get column widths
		System.out.println("\nTEST: GET COLUMN WIDTHS");
		int[] widths = df.getColumnWidths();
		for(int width : widths)
		{
			System.out.println(width);
		}
	}
}
