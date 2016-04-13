""" Xiaozheng Xu's code for recursive art video frames generator """       
import random
import os
import shutil
from math import sin, cos, pi
from PIL import Image
from swampy import structshape 

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

    function_blocks=['prod','sin_pi','cos_pi','avg','max','min']
    depth=random.randint(min_depth,max_depth)

    if depth==1:
        return random.sample(['x','y','t'],1)
    else:
        function=function_blocks[random.randint(0,5)]
        if function in ['prod','avg','max','min']: #for functions that takes 2 arguments
            rand_fun_1=build_random_function(depth-1,depth-1)
            rand_fun_2=build_random_function(depth-1,depth-1)
            return [function,rand_fun_1,rand_fun_2]
        else:   # for the sin and cos functions that take 1 argument
            rand_fun=build_random_function(depth-1,depth-1)
            return [function,rand_fun]

def evaluate_random_function(f, x, y, t):
    """ Evaluate the random function f with inputs x,y,t
        Representation of the function f is a nested list (defined in the assignment writeup)

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(['x'],-0.5, 0.75,0.2)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02,0.3)
        0.02
    """
    if f[0]=="x":
        return x
    elif f[0]=="y":
        return y 
    elif f[0]=="t":
        return t
    elif f[0]=='sin_pi':
        a=evaluate_random_function(f[1],x,y,t)
        return sin(pi*a)
    elif f[0]=='cos_pi':
        a=evaluate_random_function(f[1],x,y,t)
        return cos(pi*a)
    elif f[0]=='prod':
        a=evaluate_random_function(f[1],x,y,t)
        b=evaluate_random_function(f[2],x,y,t)
        return a*b
    elif f[0]=='avg':
        a=evaluate_random_function(f[1],x,y,t)
        b=evaluate_random_function(f[2],x,y,t)
        return 0.5*(a+b)
    elif f[0]=='max':
        a=evaluate_random_function(f[1],x,y,t)
        b=evaluate_random_function(f[2],x,y,t)
        return max(a,b)
    elif f[0]=='min':
        a=evaluate_random_function(f[1],x,y,t)
        b=evaluate_random_function(f[2],x,y,t)
        return min(a,b)


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    ratio=float(val-input_interval_start)/(input_interval_end-input_interval_start)
    output_value=ratio*(output_interval_end-output_interval_start)+output_interval_start
    return output_value 

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(150, 255),  # Red channel
                            random.randint(0, 50),  # Green channel
                            random.randint(0, 150))  # Blue channel

    im.save('./Softdes/ComputationalArt/movie1/'+filename,'PNG')


def generate_art(filename, t, red_function,green_function,blue_function, order, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (#0,
                    color_map(evaluate_random_function(red_function, x, y,t)),
                    color_map(evaluate_random_function(green_function, x, y,t)),
                    color_map(evaluate_random_function(blue_function, x, y,t))
                    )

    im.save('/home/xiaozheng/Softdes/ComputationalArt/movie_frames/movie'+str(order)+'/'+filename)


def make_movie(beg,end,function_num,order):
    '''This movie makes the frames of a movie from chosen red function, green function and blue function. 
    beg is the starting frame number, end is the end frame number, and end-beg is the number of frames generated'''
    red_function=red_functions[function_num]
    green_function=green_functions[function_num]
    blue_function=blue_functions[function_num]
    for t in range(beg,end): 
        t_remaped=remap_interval(t,beg,end,-1,1)
        file_name='{}{}{}'.format('frame',t,'.png')
        generate_art(file_name,t_remaped,red_function,green_function,blue_function,order)


red_functions=[]
green_functions=[]
blue_functions=[]

def choose_function(order,num_of_choices):
    '''Generate movie function candidates for the user to choose from. Order is the movie folder number. '''
    for i in range(num_of_choices):
            red_function = build_random_function(7, 9)
            green_function = build_random_function(7, 9)
            blue_function = build_random_function(7, 9) 
            red_functions.append(red_function)
            green_functions.append(green_function)
            blue_functions.append(blue_function)
            file_name_i='{}{}{}'.format('candidate',i,'i.png')
            file_name_f='{}{}{}'.format('candidate',i,'f.png')
            generate_art(file_name_i,-1,red_function,green_function,blue_function,order)
            generate_art(file_name_f,1,red_function,green_function,blue_function,order)

def generate_movie():
    order=int(raw_input('Please enter the movie number you want to make: '))
    try:
        os.mkdir('/home/xiaozheng/Softdes/ComputationalArt/movie_frames/movie'+str(order))
    except OSError:
        pass    

    num_of_choices=int(raw_input('Please enter how many candidate pictures you want to choose from:'))

    choose_function(order,num_of_choices)
    user_input=raw_input('Please enter the picture you want to make into movie:(1,2,3,4...etc)')

    candidate_nums=user_input.split(',')  

    for i,num in candidate_nums:   #num is a string of an integer 
        movie_num=int(num)
        if i>0:
            try:
                os.mkdir('/home/xiaozheng/Softdes/ComputationalArt/movie_frames/movie'+str(order+i))
            except OSError:
                pass
        make_movie(0,100,movie_num,order+i)

        for i in range(99):
            shutil.copyfile('/home/xiaozheng/Softdes/ComputationalArt/movie_frames/movie'+str(order+i)+'/frame'+str(i)+'.png',
             '/home/xiaozheng/Softdes/ComputationalArt/movie_frames/movie'+str(order+i)+'/frame'+str(198-i)+'.png')


generate_movie()

#doctest
if __name__ == '__main__':
    import doctest
    doctest.testmod()
