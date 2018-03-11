package extractor;

import org.jetbrains.annotations.Contract;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Extractor {

	private static List<String> stringList;

	public Extractor() throws IOException, InterruptedException {
		process();
		stringList = readFromFile("/Users/jayantsingh/Desktop/Project/src/extractor/linkList.dat");
	}

	private void process() throws IOException, InterruptedException {
		System.out.println("process started ... ");
		String command[] = {"python3", "/Users/jayantsingh/Desktop/Project/src/extractor/script/Trends.py"};
		ProcessBuilder processBuilder = new ProcessBuilder(command);
		Process process = processBuilder.start();
		processBuilder.redirectErrorStream(true);
		BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
		String s = " ";
		while ((s = bufferedReader.readLine())!=null) {
			System.out.println(s);
		}
		int exitCode = process.waitFor();
		System.out.println("Exit Code : " + exitCode);
		System.out.println("process finished");
	}

	public List<String> readFromFile(String path) throws IOException {
		List<String> lines = Files.readAllLines(Paths.get(path));
		return lines;
	}

	@Contract(pure = true)
	public static List<String> getList() {
		return stringList;
	}
}
