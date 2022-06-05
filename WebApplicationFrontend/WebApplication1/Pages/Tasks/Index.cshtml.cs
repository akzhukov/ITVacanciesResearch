using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Logging;

namespace WebApplication1.Pages.Tasks
{
    using NameLink = KeyValuePair<string, string>;
    public class TasksModel : PageModel
    {
        private readonly ILogger<TasksModel> _logger;
        public string openedFrame;
        public string openedFrameKey;
        public const string FileName = "Tasks.txt";
        public Dictionary<string, NameLink> frames = new Dictionary<string, NameLink>();
        public TasksModel(ILogger<TasksModel> logger)
        {
            _logger = logger;
            string[] tasks = System.IO.File.ReadAllLines(Path.Combine(Directory.GetCurrentDirectory(), FileName));
            System.IO.File.WriteAllLines(@"D:\diplomMaga\test.txt", new string[] { Path.Combine(Directory.GetCurrentDirectory(), FileName) });
            int i = 1;
            foreach(var task in tasks)
            {
                var nameLink = task.Split(";");
                frames.Add($"task{i++}", new NameLink(nameLink[0], nameLink[1]));
            }
            openedFrameKey = null;
        }
        public void OnGet()
        {

        }

        public void OnPost()
        {
        }

        public IActionResult OnGetUpdate()
        {
            StartServices.StartDBUpdate();
            return Redirect("/");
        }

        public void OnPostOpenTask(string key)
        {
            openedFrame = frames[key].Value;
            openedFrameKey = key;
            //return Page();
        }


    }
}
