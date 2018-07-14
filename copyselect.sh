#!/bin/bash -l

#SBATCH --export=NONE
#SBATCH --account=mwasci
#SBATCH --clusters=zeus
#SBATCH --time=12:00:00
#SBATCH --output=/astro/mwasci/duchesst/copyselect.o%A
#SBATCH --error=/astro/mwasci/duchesst/copyselect.e%A
#SBATCH --nodes=1
#SBATCH --tasks=4
#SBATCH --cpus-per-task=1 
#SBATCH --partition=copyq

module load mpifileutils

start_time=`date +%s`

delete_old=false
overwrite_existing=false

DOWNLOAD=download
CAL=cal
MODEL=model
IMAGE=image
FINAL=fnlimage

# Read the options
TEMP=`getopt -o a:b:c:d:e:fg --long output_dir:,obsid_list:,select:,ext:,input_dir:,delete,overwrite -- "$@"`
eval set -- "$TEMP"

# Extract options and their arguments into variables
while true ; do
    case "$1" in
        -a|--output_dir) # output directory (required argument)
            case "$2" in
                "") shift 2 ;;
                *) output_dir=$2 ; shift 2 ;;
            esac ;;
        -b|--obsid_list) # obsID list (required argument)
            case "$2" in
                "") shift 2 ;;
                *) obsid_list=$2 ; shift 2 ;;
            esac ;;
        -c|--select) # rows to select in obsID list, e.g. 1 or 1-10 (required argument)
            case "$2" in
                "") shift 2 ;;
                *) select=$2 ; shift 2 ;;
            esac ;;
        -d|--ext) # rows to select in obsID list, e.g. 1 or 1-10 (required argument)
            case "$2" in
                "") shift 2 ;;
                *) ext=$2 ; shift 2 ;;
            esac ;;
        -e|--input_dir) # rows to select in obsID list, e.g. 1 or 1-10 (required argument)
            case "$2" in
                "") shift 2 ;;
                *) input_dir=$2 ; shift 2 ;;
            esac ;;
        -f|--delete) delete_old=true ; shift ;;
        -g|--overwrite) overwrite_existing=true ; shift ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done

# Check required arguments have been specified
if [ -z "$output_dir" ]; then
    echo "Error: output_dir not specified. Aborting."
    exit 1
elif [ -z "$obsid_list" ]; then
    echo "Error: obsid_list not specified. Aborting."
    exit 1
elif [ -z "$select" ]; then
    echo "Error: select not specified. Aborting."
    exit 1
elif [ -z "$input_dir" ]; then
	echo "Error: input_dir not specified. Aborting."
	exit 1
fi


# Create output directory
if [ ! -e $output_dir ]; then
    mkdir $output_dir  
fi


# Determine list of pointings to image then download:
start=${select%-*}
end=${select#*-}
i=0

obsids=()
while read line || [[ -n "$line" ]]; do
    (( i++ ))
    if [ $(echo "$i >= $start"|bc) -eq 1 ] && [ $(echo "$i <= $end"|bc) -eq 1 ]; then
    	obsid=`echo "$line" | awk '{print $1}'`
        obsids+=($obsid)
    fi
done < $obsid_list

if $overwrite_existing; then
    overwrite_option="-f"
else
    overwrite_option=""
fi

for obsid in ${obsids[@]}; do
    # Move everything possible to /group:
    # or move things back from /group to /astro!
    for d in $DOWNLOAD $CAL $MODEL; do

        if [ ! -e ${output_dir}/${d} ]; then
            mkdir ${output_dir}/${d}
        fi

        echo "Moving ${input_dir}/${d}/${obsid} to ${output_dir}/${d}"

        mpirun -np 4 dcp -p ${overwrite_option} ${input_dir}/${d}/${obsid} ${output_dir}/${d}

        if $delete_old; then
            echo "Removing ${d}${ext}/${obsid} from /astro..."
            find ${input_dir}/${d}/${obsid} -type f -print0 | xargs -0 munlink
            find ${input_dir}/${d}/${obsid} -depth -type d -empty -delete
        fi


    done

    for d in $IMAGE $FINAL; do

        if [ ! -e ${output_dir}/${d}${ext} ]; then
            mkdir ${output_dir}/${d}${ext}
        fi

        echo "Moving ${input_dir}/${d}${ext}/${obsid} to ${output_dir}/${d}${ext}"
        mpirun -np 4 dcp -p ${overwrite_option} ${input_dir}/${d}${ext}/${obsid} ${output_dir}/${d}${ext}
        if $delete_old; then
            find ${input_dir}/${d}${ext}/${obsid} -type f -print0 | xargs -0 munlink
            find ${input_dir}/${d}${ext}/${obsid} -depth -type d -empty -delete
        fi

    done

done

end_time=`date +%s`
duration=`echo "$end_time-$start_time" | bc -l`
echo "Total runtime = $duration sec"

# Move output and error files to output directory
mv $MYDATA/copyselect.o${SLURM_JOB_ID} $MYDATA/copyselect.e${SLURM_JOB_ID} .