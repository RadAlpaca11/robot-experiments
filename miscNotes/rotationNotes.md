# Euler rotation to quaternions

https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html

## Questions
* Does genesis use scalar first or last quaternions?
    * Scalar first 
* Genesis has a get_quat() function, but not a get_euler() function. 
* Genesis's euler properties follow scipy's extrinsic rotation convention.
* Is the output from openPi use scalar first or last quaternions?

## Thoughts
* We have to get the current quat from the model. We can then either convert the current quat to euler, use the euler output, and set the euler in qpos. Or we can convert the euler output to quat and just use the quat output. (for cogact and openvla)