This feature is provided by https://glot.io (whose github webpage is https://github.com/prasmussen/glot-run/) and its associated api. Example:
  ```c#
     >> exe c#
        class MainClass {
            static void Main() {
                System.Console.WriteLine("Hello World!");
            }
        }
       --------------------------------------
        stdout: Hello World!
        stderr: 
        error: 
  ```

You must visit the page above to create a free account and then go to https://glot.io/account/token to obtain an api key. fill in the key in the `GLOT_RUN_TOKEN` variable in the file `config_bot.py`.