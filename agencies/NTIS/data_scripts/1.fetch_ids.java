import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

public class fetch_ids {

	public static void getpages() throws InterruptedException, IOException {
		// 2005-2006 incomplete
		String start = "2016";
		String end = "2017";

		// NOTE: find these short hand for years manually looking at the html of the page
		String st = "117";
		String en = "0";

		String folderpath = "";

		Writer writer = new BufferedWriter(
				new OutputStreamWriter(new FileOutputStream(folderpath + start + "-" + end + ".txt"), "utf-8"));

		System.setProperty("webdriver.firefox.bin", "/Applications/Firefox2.app/Contents/MacOS/firefox-bin");
		WebDriver driver = new FirefoxDriver();
		driver.get("https://ntrl.ntis.gov");
		driver.manage().window().maximize();
		Thread.sleep(4000);

		driver.findElement(By.xpath("//label[@id='advSearchForm:FromYear_label']")).click();

		driver.findElement(By.id("advSearchForm:FromYear_filter")).sendKeys(String.valueOf(start));

		driver.findElement(By.id("advSearchForm:FromYear_" + st)).click();

		driver.findElement(By.xpath("//label[@id='advSearchForm:ToYear_label']")).click();

		driver.findElement(By.id("advSearchForm:ToYear_filter")).sendKeys(String.valueOf(end));

		driver.findElement(By.id("advSearchForm:ToYear_" + en)).click();

		driver.findElement(By.id("advSearchForm:advSearchSubmit")).click();

		Thread.sleep(6000);

		// NOTE: select '100' in the drop down menu manually

		writer.write(driver.findElement(By.className("ui-paginator-current")).getText() + "\n");

		while (true) {

			List<WebElement> rows = null;

			while (true) {
				try {
					Thread.sleep(3000);

					rows = driver.findElement(By.id("searchResultsForm:searchResultsTable_data"))
							.findElements(By.tagName("tr"));
					for (WebElement row : rows) {

						String abbr = row.findElement(By.className("searchResultsAbbr")).getText();
						writer.write(abbr + "\n");
						writer.flush();
						// System.out.println(abbr);
					}

				} catch (Exception e) {
					Thread.sleep(3000);
					System.out.println("Error! waiting for 3 secs");
					continue;
				}
				break;
			}

			WebElement nextpage = driver.findElement(By.xpath("//a[@aria-label='Next Page']"));

			String able = nextpage.getAttribute("class");

			if (able.contains("disabled")) {
				break;

			}

			nextpage.click();

		}

		writer.close();

	}

	public static void main(String[] args) throws InterruptedException, IOException {
		getpages();
	}
}
