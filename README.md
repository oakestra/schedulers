# Oakestra Schedulers

Task schedulers for Oakestra. We differenciate between Root, Cluster and Generic scheduler. 

A Root scheduler given a task returns a list of cluster candidates.

A Cluster scheduler given a task returns a list of worker candidates. 

A Generic scheduler, given a generic resource, returns a list of candidates. These non specialized schedulers are suitable for both Root and Cluster orchestrators. 


