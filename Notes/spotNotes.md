## Spot anatomy/DOF notes:

- [boston dynamics documentation](https://dev.bostondynamics.com/docs/concepts/about_spot) was helpful
- 12 dof total
- 3 on each leg
	- hip x (hx)
	- hip y (hy)
	- knee (kn)
- hips are ball joints
- legs are labeled like this:
	-front left = fl
	-hind  right = hr
- hind left knee joint = hl_kn
- joint index:

        jnt_names = [
            'fl_hx',
            'fl_hy',
            'fl_kn',
            'fr_hx',
            'fr_hy',
            'fr_kn',
            'hl_hx',
            'hl_hy',
            'hl_kn',
            'hr_hx',
            'hr_hy',
            'hr_kn',
        ]
        dofs_idx = [spot.get_joint(name).dof_idx_local for name in jnt_names]


- hx range = -0.785398 0.785398
- hy range = -0.898845 2.24363
- kn range = -2.7929 -0.247067
 
- 0 isn't in knee range?
- is 0 straight?
- might be worth looking further into spot documentation
- what happens if force value is negative?
