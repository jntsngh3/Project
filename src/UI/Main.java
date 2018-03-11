package UI;

import extractor.Extractor;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{

        /**
         *
         */
        Parent root = FXMLLoader.load(getClass().getResource("ui_layout.fxml"));
        primaryStage.setTitle("Something in the World");
        primaryStage.setScene(new Scene(root));
        primaryStage.show();

    }


    public static void main(String[] args) throws IOException, InterruptedException {
        new Extractor();
        launch(args);
    }
}
