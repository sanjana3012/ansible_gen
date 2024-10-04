
import argparse

medium={"vcpu": 2, "ram": 2, "disk": 20}
large={"vcpu": 4, "ram": 8, "disk": 40}

###################################
#
# Parse command line arguments
#
###################################
def parseCmdLineArgs ():
  # instantiate a ArgumentParser object
  parser = argparse.ArgumentParser (description="chord test")
  
  parser.add_argument ("-b", "--bastion", type=int, default=1, help="Number of bastion hosts (default 1)")
  parser.add_argument ("-c", "--clusters", type=int, default=24, help="Number of clusters (teams - default 24)")
  parser.add_argument ("-f", "--flavor", default="large", help="Flavor used by master (default large, choices: large and medium)")
  parser.add_argument ("-m", "--masters", type=int, default=1, help="Number of masters per cluster (default 1)")
  parser.add_argument ("-w", "--workers", type=int, default=3, help="Number of workers per cluster (default 3)")
  
  return parser.parse_args()


###################################
#
# Main program
#
###################################
def main ():


  args = parseCmdLineArgs ()

  bastion_flavor = large
  if (args.flavor == "large"):
    master_flavor = large
    worker_flavor = medium
  else:
    master_flavor = medium
    worker_flavor = medium
    
  instances = args.bastion + args.clusters*args.masters + args.clusters*args.workers
  total_vcpu = args.bastion*bastion_flavor["vcpu"] + args.clusters*args.masters*master_flavor["vcpu"] + args.clusters*args.workers*worker_flavor["vcpu"]
  total_ram = args.bastion*bastion_flavor["ram"] + args.clusters*args.masters*master_flavor["ram"] + args.clusters*args.workers*worker_flavor["ram"]
  total_disk = args.bastion*bastion_flavor["disk"] + args.clusters*args.masters*master_flavor["disk"] + args.clusters*args.workers*worker_flavor["disk"]

  print ("Total instances = {}, vcpu = {}, ram = {} and disk = {}".format (instances, total_vcpu, total_ram, total_disk))


    
###################################
#
# Main entry point
#
###################################
if __name__ == "__main__":

  main ()
