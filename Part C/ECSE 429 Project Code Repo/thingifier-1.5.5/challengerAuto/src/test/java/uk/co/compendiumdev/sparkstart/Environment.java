package uk.co.compendiumdev.sparkstart;


import spark.Spark;
import uk.co.compendiumdev.challenge.ChallengeMain;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class Environment {

    public static boolean SINGLE_PLAYER_MODE = false;

    public static String getEnv(String urlPath){
        return  getBaseUri() + urlPath;
    }

    public static String getBaseUri() {

        // return environment if want to run externally
//        if(true)
//            return "https://apichallenges.herokuapp.com";

        int port = 5000;
        // if not running then start the spark
        if(Port.inUse("localhost", port)) {
            return "http://localhost:" + port;
        }else{
            //start it up
            Spark.port(port);
            String [] args;

            if(SINGLE_PLAYER_MODE){
                args = "".split(",");
            }else{
                args = "-multiplayer".split(",");
            };


            ChallengeMain.main(args);

            // wait till running
            int maxtries=10;
            while(!Port.inUse("localhost", port)){
                maxtries--;
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            return "http://localhost:" + port;
        }

        // TODO: incorporate browsermob proxy and allow configuration of all
        //  requests through a proxy file to output a HAR file of all requests for later review
    }
}
