package UI;

import extractor.Extractor;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;

import java.io.IOException;
import java.net.URL;
import java.util.List;
import java.util.ResourceBundle;

public class LayoutController implements Initializable{

	ObservableList observableList = FXCollections.observableArrayList();

	@FXML
	private ListView linkList = new ListView(observableList);

	@FXML
	private WebView webView = new WebView();

	@Override
	public void initialize(URL location, ResourceBundle resources) {
		pouplateList();
	}

	private void loadURL(String URL){
		WebEngine engine = webView.getEngine();
		engine.load(URL);
	}

	private void pouplateList() {
		List<String> stringList = Extractor.getList();
		observableList.addAll(stringList);
		linkList.setItems(observableList);
		linkList.setOnMouseClicked(event -> {
			String string = linkList.getSelectionModel().getSelectedItems().toString();
			loadURL(string.substring(1, string.length()-1));
		});
	}
}
