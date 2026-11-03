// Import this first in every script that reads or writes job files. All of them use the current folder as the job,
// so a script run from the wrong folder would scatter files there. This stops it before it writes anything.
import { die } from "./config.mjs";
import { jobProblem } from "./project.mjs";

const problem = jobProblem();
if (problem) die(problem);
