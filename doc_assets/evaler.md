This feature is provided by https://glot.io (whose github webpage is https://github.com/prasmussen/glot-run/) and its associated api. Example:
  ```
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

You must visit the page above to create a free account and then go to https://glot.io/account/token to obtain an api key. fill in the key in the `TOKEN` variable in the file `data_source_glot_run.py`.